import React from "react";
import { Button } from "react-bootstrap";
import Link from "../components/Helpers/Link";
import Base from "../components/Base";

const NotFoundPage = () => (
  <Base>
    <div className="row justify-content-center">
      <div className="col-xs-12 col-lg-8 text-center">
        <h1 style={{ fontSize: "8rem", color: "#ce1664" }}>404</h1>
        <p>The page you are looking for was moved, removed, renamed or may have never existed.</p>

        <div className="my-2">
          <Button as={Link} href="/">
            Site Home
          </Button>
          <Button as={Link} href="/blog/" className="ml-1">
            Blog Feed
          </Button>
        </div>

        <small className="text-muted">
          If you think this was an issue or were sent here by a link, feel free to{" "}
          <Link href="/about/#contact">contact me</Link> and I will look into the URL.
        </small>
      </div>
    </div>
  </Base>
);

export default NotFoundPage;
