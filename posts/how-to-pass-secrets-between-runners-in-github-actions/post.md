title: "How to Pass Secrets Between Runners in GitHub Actions"
date: 2022-06-15
category: Tutorials
tags: [github]
feature: feature.png
description: "When trying to pass a secret or masked variable between jobs in GitHub Actions using outputs, it will say \"Warning: Skip output '' since it may contain secrets\". This tutorial aims to provide a reasonable solution for this."

[TOC]

## The Issue

When trying to pass a secret or masked variable between jobs in GitHub Actions using outputs, it will say *"Warning: Skip output '' since it may contain secrets"*. GitHub states in their ["Defining outputs for jobs" docs](https://docs.github.com/en/actions/using-jobs/defining-outputs-for-jobs#overview):

> Job outputs containing expressions are evaluated on the runner at the end of each job. Outputs containing secrets are redacted on the runner and not sent to GitHub Actions.

### My Problematic Scenario

In my scenario, I have a job that deploys my infrastructure and then passes deployment keys to other jobs so they can run in parallel. Here is a small example of the flow:

![Flow Example](/posts/how-to-pass-secrets-between-runners-in-github-actions/flow-example.png)

My infrastructure job looks a bit like this:

```yaml
jobs:
  # ...
  
  deploy-infrastructure:
    name: "Deploy Infrastructure"
    runs-on: windows-latest
    outputs:
      deployment_key_for_api: ${{ steps.set_outputs.outputs.deployment_key_for_api }}
      deployment_key_for_client: ${{ steps.set_outputs.outputs.deployment_key_for_client }}
    steps:
      - uses: actions/checkout@main

      # ...

      - name: Set outputs
        id: set_outputs
        run: |
          $deployment_key_for_api = "Method of obtaining this has been removed for simplicity..."
          echo "::add-mask::$deployment_key_for_api"
          echo "::set-output name=deployment_key_for_api::$deployment_key_for_api"

          $deployment_key_for_client = "Method of obtaining this has been removed for simplicity..."
          echo "::add-mask::$deployment_key_for_client"
          echo "::set-output name=deployment_key_for_client::$deployment_key_for_client"
```

And one of the jobs that uses this output looks like:


```yaml
jobs:
  # ...

  deploy-server:
    name: "Deploy Server"
    needs: deploy-infrastructure
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@main

      # ...

      - name: Get Deploy Key
        id: get_deploy_key
        shell: bash
        run: |
          $deployment_key="${{ needs.deploy-infrastructure.outputs.deployment_key_for_api }}"
          echo "::add-mask::$deployment_key"
          echo "::set-output name=deployment_key::$deployment_key"

      # Uses ${{ steps.get_deploy_key.outputs.deployment_key }} later...
```

You would have seen that I'm using `::add-mask::` above - this is used to stop GitHub Actions logs showing my secrets. Unfortunately once a mask is applied to a value, that value cannot be passed between runners.

Since each job runs on their own "runner" (a completely different VM / agent), outputs are passed back to GitHub Actions which are then passed back to the runner for the new job that needs them. Since I'm trying to pass a secret / masked value using outputs, the runner will redact any outputs containing secrets and not send them to GitHub Actions (as stated in the GitHub docs) to be passed on to the next job.

This is the warning I see:

![GitHub Actions skip because of secret/mask](/posts/how-to-pass-secrets-between-runners-in-github-actions/ga-skip-because-of-secret.png)


And here is my value missing in the later job:

![GitHub Actions skip leads to an empty value](/posts/how-to-pass-secrets-between-runners-in-github-actions/ga-skip-leads-to-empty-value.png)


## The Solution

While looking for a solution, I found [this GitHub issue](https://github.com/actions/runner/issues/1498) which gave me the idea of encrypting secrets being passed between runners/jobs.

Pretty much the idea is to symmetrically encrypt the secret/masked value using PGP in the source runner and decrypt it in the designation runner. This means you can still mask the value from the logs but the actual value being passed around is not the masked value.

Before you can symmetrically encrypt/decrypt a value with PGP, you need a passphrase. We can't generate this on the go as passing it to the next job would mean it either shows in the logs, or can't be sent over as it is masked! An easy way around this is to create a secret in GitHub Actions for the repo that is to be used only for this task - something like "`PGP_SECRET_SIGNING_PASSPHRASE`".

To encrypt a value in bash, we can use:

```
encrypted_value=$(gpg --symmetric --batch --passphrase "SECRET" --output - <(echo "my-secret-string") | base64 -w0)
```

You hopefully have noticed a couple of things above:

- This is being assigned to a variable - so you can set it as an output
- "`--output -`"? - this outputs the encrypted value to stdout which is picked up the by "$()"
- "`<`"? - this redirects the value being echoed into stdin (to be encrypted)
- "`| base64 -w0`"? - this outputs the encrypted value to base64 without any line breaks (so we aren't just passing bytes that may break across runners)

To decrypt the above value, we can then use:

```
decrypted_value=$(gpg --decrypt --quiet --batch --passphrase "SECRET" --output - <(echo "$encrypted_value" | base64 --decode))
```

Using the two commands above together, you should see "my-secret-string" when executing "`echo $decrypted_value`".


So the steps to solve this issue are:

1. Create a new secret with your PGP signing key (e.g. `PGP_SECRET_SIGNING_PASSPHRASE`)
2. Encrypt the output in the source job
3. Decrypt the output of the dependant job in the destination job

### Example

Here is an example of how I performed these steps between jobs.

First, I defined a secret in GitHub Actions called `PGP_SECRET_SIGNING_PASSPHRASE` with a long random value that I will never need to see again.


Then I updated my pipeline to encrypt my secrets before using them as outputs:

```yaml
jobs:
  deploy-infrastructure:
    name: "Deploy Infrastructure"
    runs-on: windows-latest
    outputs:
      deployment_key_for_api_encrypted: ${{ steps.set_outputs.outputs.deployment_key_for_api_encrypted }}
      deployment_key_for_client_encrypted: ${{ steps.set_outputs.outputs.deployment_key_for_client_encrypted }}
    steps:
      - uses: actions/checkout@main

      # ...

      - name: Set outputs
        id: set_outputs
        shell: bash
        run: |
          deployment_key_for_api="Method of obtaining this has been removed for simplicity..."
          echo "::add-mask::$deployment_key_for_api"
          deployment_key_for_api_encrypted=$(gpg --symmetric --batch --passphrase "$SECRET" --output - <(echo "$deployment_key_for_api") | base64 -w0)
          echo "::set-output name=deployment_key_for_api_encrypted::$deployment_key_for_api_encrypted"

          deployment_key_for_client="Method of obtaining this has been removed for simplicity..."
          echo "::add-mask::$deployment_key_for_client"
          deployment_key_for_client_encrypted=$(gpg --symmetric --batch --passphrase "$SECRET" --output - <(echo "$deployment_key_for_client") | base64 -w0)
          echo "::set-output name=deployment_key_for_client_encrypted::$deployment_key_for_client_encrypted"
        env:
          SECRET: ${{ secrets.PGP_SECRET_SIGNING_PASSPHRASE }}

  deploy-server:
    name: "Deploy Server"
    needs: deploy-infrastructure
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@main

      # ...

      - name: Get Deploy Key
        id: get_deploy_key
        shell: bash
        run: |
          deployment_key=$(gpg --decrypt --quiet --batch --passphrase "$SECRET" --output - <(echo "${{ needs.deploy-infrastructure.outputs.deployment_key_for_api_encrypted }}" | base64 --decode))
          echo "::add-mask::$deployment_key"
          echo "::set-output name=deployment_key::$deployment_key"

      # Uses ${{ steps.get_deploy_key.outputs.deployment_key }} later...
```