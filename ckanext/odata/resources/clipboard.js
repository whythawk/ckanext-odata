ckan.module('clipboard', function (jQuery, _) {
  return {
      initialize: function () {
      var el = this.el
      var $copy = $('<span> <i title="Copy to clipboard" class="icon-paste"></i></span>');
      el.append($copy);
      $copy.clipboard({
        path: '/jquery.clipboard.swf',
        copy: function() {
            return el.text();
      }});
    }
  };
});
