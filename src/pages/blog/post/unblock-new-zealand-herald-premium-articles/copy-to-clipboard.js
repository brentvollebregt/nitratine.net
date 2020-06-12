function copyCode() {
    let content = "javascript:window.prtn = { f: btoa(window.env.HASH + window.location.href) };isMobile.any = () => true;$('head').append(    '<style>' +        '#main { height: auto !important; } ' +'#article-content { height: auto !important; overflow: auto !important; } ' +        '#article-content > * { display: block !important; color: #000 !important; opacity: 1 !important; } ' +        '.article-offer { display: none !important; } ' +        '.ad-container, .pb-f-article-related-articles { display: none !important; } ' +    '</style>');function mode(arr) {    return arr.sort((a,b) =>          arr.filter(v => v===a).length        - arr.filter(v => v===b).length    ).pop();}let article_content = $('#article-content');let classes = [];article_content.children().each((index, e) => {    e.classList.forEach(i => classes.push(i));});let possible_premium_class = mode(classes);$('.' + possible_premium_class).css('display', '').removeClass(possible_premium_class);article_content    .removeClass('premium-content')    .addClass('full-content');";
    let textarea = document.createElement("textarea");
    textarea.textContent = content;
    document.body.appendChild(textarea);
    textarea.select();
    if (!document.execCommand("copy")) {
        window.prompt("Copy this then click OK", content);
    }
    textarea.remove();
    document.getElementById('copyCodeSuccess').style.display = 'block';
    setTimeout(function(){ document.getElementById('copyCodeSuccess').style.display = 'none'; }, 2000);
}
