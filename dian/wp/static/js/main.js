Zepto(function($) {
  console.log('haha');
  $('input[name=table_type]').change(function () {
    $('.table-type-wrap label').removeClass('active');
    $(this).next().toggleClass('active');
  });
  $('input[name="table_type"]').closest('label').toggleClass('active');
})
