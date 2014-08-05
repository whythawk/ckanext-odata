ckan.module('odata_copy', function (jQuery, _) {
  return {
      initialize: function () {
      var el = this.el;
      var select = el.find(".odata-select");
      var input = el.find('input');
      input.css( 'cursor', 'default' );
      var show = false;
      var sel = el.find('input').attr('readonly', true)
      sel.focus(function () {
        this.select()
                input.select();
                select.show();
      });
      sel.blur(function () {
                select.hide();
      });
      sel.click(function () {
                input.select();
      });
      el.find(".odata-label").click( function (){
                input.focus();
      });
    }
  };
});
