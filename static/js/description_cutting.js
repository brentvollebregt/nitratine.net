document.getElementsByTagName('body')[0].onresize = function () {
    var class_tile = Array.prototype.slice.call(document.getElementsByClassName('tile'), 0);
    var class_date_order_article = Array.prototype.slice.call(document.getElementsByClassName('date_order_article'), 0);
    var tiles = class_tile.concat(class_date_order_article);
    for (var i = 0; i < tiles.length; i++) {
        var tile = tiles[i];
        var p = tile.getElementsByClassName('tile_text')[0];
        var stats = tile.getElementsByClassName('tile_tag_box')[0];
        var height = stats.getBoundingClientRect().top - p.getBoundingClientRect().top;
        p.style.maxHeight = height + "px"
    }
};

window.onload = document.getElementsByTagName('body')[0].onresize;