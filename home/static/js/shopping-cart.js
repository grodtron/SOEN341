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

   var updateButtons = function(cart){
      $('.shopping-btn').each(function(i, btn){
         setButtonAdd($(btn));
      });
      $.each(cart, function(i, course){
         var btn = $("#shopping-btn-" + course.course_id); 
         setButtonRemove(btn);
      });
   }

   var setButtonAdd = function(btn){
      btn
         .unbind('click')
         .button('add')
         .removeClass('btn-primary')
         .addClass('btn-success')
         .bind('click', onclickAdd)
   }

   var setButtonRemove = function(btn){
      btn
         .unbind('click')
         .button('remove')
         .removeClass('btn-primary')
         .addClass('btn-danger')
         .bind('click', onclickRemove)
   }

   var setButtonLoading = function(btn){
      btn
         .unbind('click')
         .button('loading')
         .removeClass('btn-success')
         .removeClass('btn-danger')
         .addClass('btn-primary')
   }

   var onclickRemove = function(){
      var btn = $(this); 

      setButtonLoading(btn);

      $.ajax("/shopping-cart/do-remove",
         {
            type:"POST",
            dataType:"json",
            data:{ course : btn.data("id") },
            success:function(data, textStatus, jqXHR){
               setButtonAdd(btn);
               updateBadge(data.length);
               updateSidebar(data);
            },
            error:function(jqXHR, textStatus, errorThrown){
               setButtonRemove(btn);
            }
         });
   };

   var onclickAdd = function(){
      var btn = $(this); 

      setButtonLoading(btn);

      $.ajax("/shopping-cart/do-add",
         {
            type:"POST",
            dataType:"json",
            data:{ course : btn.data("id") },
            success:function(data, textStatus, jqXHR){
               setButtonRemove(btn);
               updateBadge(data.length);
               updateSidebar(data);
            },
            error:function(jqXHR, textStatus, errorThrown){
               setButtonAdd(btn);
            }
         });
   };

   // Initialize the whole thing
   $.ajax("/shopping-cart/get-cart",
   {
      dataType:"json",
      success:function(data){
         updateBadge(data.length);
         updateSidebar(data);
         updateButtons(data);
      }
   });
         
});
