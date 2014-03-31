$(document).ready(function(){

   var updateCart = function(n_items){
      $("#shopping-cart-badge").text(n_items);
   }

   $.ajax("/shopping-cart/get-cart",
      {
         dataType:"json",
         success:function(data){
            updateCart(data.length);
            // TODO - disable buttons of items already in cart
         }
      });

   $(".shopping-btn").bind("click", function(){
      var btn = $(this); 
      btn
         .button('loading')
         .unbind("click");

      $.ajax("/shopping-cart/do-add",
         {
            type:"POST",
            dataType:"json",
            data:{ course : btn.data("id") },
            success:function(data, textStatus, jqXHR){
               btn
                  .button('reset')
                  .removeClass('btn-primary')
                  .addClass('btn-success');
               updateCart(data.length);
            },
            error:function(jqXHR, textStatus, errorThrown){
               btn
                  .button('reset')
                  .removeClass('btn-primary')
                  .addClass('btn-sdanger')
            }
         });

      this.onclick
   });
});
