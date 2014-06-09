ckan.module('clipboard', function (jQuery, _) {
  return {
      initialize: function () {
      var $copy = $('<span> <i title="Copy to clipboard" class="icon-paste"></i></span>');
      $copy.clipboard({
        path: '/jquery.clipboard.swf',
        copy: function() {
            alert('Text copied. Try to paste it now!');
            return $(this.el).text();
      }});
      this.el.append($copy);
    }
  };
});
