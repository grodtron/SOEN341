$(document).ready(function(){

   var updateBadge = function(nItems){
      $("#shopping-cart-badge").text(nItems);
   }

   var updateSidebar = function(cart){
      var table = $("#wishlist-sidebar");
      table.empty();

      if(cart.length > 0){
         $.each(cart, function(i, course){
            table.append(
               '<tr><td><b>'
               + course['course_code']
               + '</b> - '
               + course['course_name']
               + '</td></tr>');
         });
      }else{
         table.append('<tr><td>No courses currently added</td></tr>');
      }
   }

   var setButtonChecked = function(btn){
      btn
         .button('complete')
         .removeClass('btn-primary')
         .addClass('btn-success');
      
   }

   var updateButtons = function(cart){
      $.each(cart, function(i, course){
         var btn = $("#shopping-btn-" + course.course_id); 
         setButtonChecked(btn);
      });
   }

   $.ajax("/shopping-cart/get-cart",
      {
         dataType:"json",
         success:function(data){
            updateBadge(data.length);
            updateSidebar(data);
            updateButtons(data);
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
               setButtonChecked(btn);
               updateBadge(data.length);
               updateSidebar(data);
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
