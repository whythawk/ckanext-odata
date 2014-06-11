ckan.module('clipboard', function (jQuery, _) {
  return {
      initialize: function () {
      var el = this.el
      el.clipboard({
         path: '/jquery.clipboard.swf',
         copy: function() {
            function crawl(el, attr){
              // find the colour going up the dom as needed
              var v = el.css(attr);
              if (v != 'rgba(0, 0, 0, 0)' && v != 'transparent'){
                return v;
              }
              if (el.prop("tagName") == 'BODY'){
                return ('#FFF')
              };
              return crawl(el.parent(), attr);
            }
            var c1 = crawl(el, 'color');
            var c2 = crawl(el, 'background-color');
            el.css({'color': c2, 'background-color': c1});
            setTimeout( function(){
                el.css({'color': c1, 'background-color': c2})}
                , 100);
             return el.find('.data').text();
      }});
    }
  };
});
