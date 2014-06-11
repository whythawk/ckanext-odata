ckan.module('clipboard', function (jQuery, _) {
  return {
      initialize: function () {
      var el = this.el
      el.clipboard({
         path: '/jquery.clipboard.swf',
         copy: function() {
            var c1 = el.css('color');
            var c2 = el.css('background-color');
            el.css({'color': c2, 'background-color': c1});
            setTimeout( function(){
                el.css({'color': c1, 'background-color': c2})}
                , 50);
             return el.find('.data').text();
      }});
    }
  };
});
