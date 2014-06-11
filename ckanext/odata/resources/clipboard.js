ckan.module('clipboard', function (jQuery, _) {
  return {
      initialize: function () {
      var el = this.el
      el.clipboard({
         path: '/jquery.clipboard.swf',
         copy: function() {
             return el.find('.data').text();
      }});
    }
  };
});
