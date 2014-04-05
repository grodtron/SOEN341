// Create Schedule Table
$( document ).ready(function() {
   var startTime = "8:45";

   $("#calendar thead").append(makeHead())

   $("#calendar tbody").append(makeRows(startTime));

   function getTempCssClass(course){
      return "temp-sched-group-" + course.course_info.schedule_item_group_id;
   }
   function getCssClass(course){
      return "sched-group-" + course.course_info.schedule_item_group_id;
   }

   var nextI = 0;

   // ABANDON HOPE ALL YE WHO ENTER HERE

   var temporary_iter_func = function(i, code, course){
      var cssClass          = getTempCssClass(course);
      var cssBackground  = "hsl("+((75*nextI)%360)+",100%,75%)"
      var cssColor       = "#000";
      return function(j, time){
         var el = insertItem(time.start, time.end, time.day);
         var div = $("<div></div>")
            .css("display", "inline-block")
            .css("position", "relative")  
            .css("width", "100%")
            .css("padding", "0px")
            .css("vertical-align" , "middle")
            .append("<h3 class='text-center noMargin'>"+course.course_info.code+"</h3>")
            .append("<p class='text-center noMargin'>"+code+"</p>");

         el
            .addClass(cssClass)
            .data("start", time.start)
            .data("day"  , time.day)
            .css("background", cssBackground)
            .css("color", cssColor)

         el.append(div);
      }
   }

   var permanent_iter_func = function(i, code, course){
      var cssClass          = getCssClass(course);
      var cssOverBackground = "hsl("+((75*nextI)%360)+",100%,40%)";
      var cssOutBackground  = "hsl("+((75*nextI)%360)+",100%,75%)";
      var cssOverColor      = "#FFF";
      var cssOutColor       = "#000";
      return function(j, time){
         var el = insertItem(time.start, time.end, time.day);
         var div = $("<div class='container-fluid'></div>")
            .css("display" , "inline-block")
            .css("position", "relative")
            .css("width", "100%")
            .css("padding", "0px")
            .css("vertical-align", "middle")
            .append("<h3 class='text-center noMargin'>"+course.course_info.code+"</h3>")
            .append("<p class='text-center noMargin'>"+code+"</p>");

         var removeBtn = $("<button type='button' class='close'>&times;</button>")
            .css("position","absolute")
            .css("top","10px")
            .css("right","10px")
            .css("z-index", "9999")
            .click(function(){
               $.ajax("/register/do-remove",
                  {
                     method:"POST",
                     data:{id:course.course_info.schedule_item_group_id},
                     success:function(){
                        $("."+cssClass).each(function(i){
                           var day   = $(this).data("day");
                           var start = $(this).data("start");
                           removeItem(start, day);
                        });
                     },
                     error:function(){
                        alert("Error removing!");
                     }
                  });
               });
            

         el.append(removeBtn);

         el
            .addClass(cssClass)
            .data("start", time.start)
            .data("day"  , time.day)
            .css("background", cssOutBackground)
            .css("color", cssOutColor)
            .hover(
               function(event){
                  $("."+cssClass)
                     .css("background", cssOverBackground)
                     .css("color", cssOverColor);
               },
               function(event){
                  $("."+cssClass)
                     .css("background", cssOutBackground)
                     .css("color", cssOutColor);
               });

         el.append(div);
      }
   }
   $.ajax("/register/get-courses",
      {
         dataType:"json",
         success:function(data){
            $.each(data, function(i, course){
               iterateOverCourseTimes(i, course, permanent_iter_func);
               ++nextI;
            });
         }
      });

   var course_dict = {}
   var get_course_and_do = function(id, callback){
      if(id in course_dict){
         callback(course_dict[id]);
      }else{
         $.ajax("register/get-course/"+id,
         {
            success:function(data){
               course_dict[id] = data;
               callback(data);
            }
         });
      }
   }

   $(".btn-reg").each(function(i){
      $(this)
         .hover(
            function(event){
               get_course_and_do($(this).data("id"), function(course){
                  var canInsert = true;
                  iterateOverCourseTimes(0, course, function(a,b,c){
                     return function(i, time){
                        if(!checkAvailability(time.start, time.end, time.day)){
                           canInsert = false;
                        }
                     }
                  });
                  if(canInsert){
                     iterateOverCourseTimes(0, course, temporary_iter_func);
                  }
               });
            },
            function(event){
               get_course_and_do($(this).data("id"), function(course){
                  var cssClass = getTempCssClass(course);
                  $("."+cssClass).each(function(i){
                     var day   = $(this).data("day");
                     var start = $(this).data("start");
                     removeItem(start, day);
                  });
               });
            }
         )
         .click(function(event){
            var id = $(this).data("id");
            $.ajax("/register/do-add",
            {
               method:"POST",
               data:{id:id},
               success:function(data){
                  get_course_and_do(id, function(course){
                     var cssClass = getTempCssClass(course);
                     $("."+cssClass).each(function(i){
                        var day   = $(this).data("day");
                        var start = $(this).data("start");
                        removeItem(start, day);
                     });
                     iterateOverCourseTimes(0, course, permanent_iter_func);
                     ++nextI;
                  });
               },
               error:function(data){
                  alert("Error: " + data.responseJSON.error);
               }
            });
            
         });
   });

});

function iterateOverCourseTimes(i, course, iter_func){

   if("lec" in course){
      $.each(course.lec.times, iter_func(
               i,
               "Lec - " +
               course.lec.section,
               course));
   }
   if("tut" in course){
      $.each(course.tut.times, iter_func(
               i,
               "Tut - " +
               course.lec.section + " " +
               course.tut.section,
               course));
   }
   if("lab" in course){
      $.each(course.lab.times, iter_func(
               i,
               "Lab - " +
               course.lec.section + " " +
               course.tut.section + " " +
               course.lab.section,
               course));
   }
}

// Used to wrap string in specific tag
function wrap(string , tag){
   pre = "<"+tag+" class='defaultClass' id='defaultId'>";
   post = "</"+tag+">";

   returnString = pre;
   returnString = returnString.concat(string);
   returnString = returnString.concat(post);

   return returnString;
}

// Increments the time by 15 minutes
function increaseTime(time){

   timeArray = time.split(":");	// split hour and minutes

   var hour = parseInt(timeArray[0]);
   var minute = parseInt(timeArray[1]);

   if (minute < 45){	// Increase time only if hour is not changing
      minute += 15;
   }
   else{				// If hour change is needed
      hour += 1;		// Change hour and reset minutes
      minute = 0;
   }

   if(minute == 0){	// Format minutes to display correctly
      minute = "00";
   }
   else{
      minute = minute.toString();
   }

   var returnTime = (hour.toString()).concat(":"+minute); 

   return returnTime;

}

// Generates all the rows needed for schedule
function makeRows(time){
   if (time === "23:30"){
      return wrap( changeClass(wrap(time , "td") , "time") +makeColumn(5) , "tr");
   }
   else{
      return wrap( changeClass(wrap(time, "td") , "time") +makeColumn(5) , "tr")+makeRows(increaseTime(time));
   }
}

// Generates all the empty td elements needed 
function makeColumn(column){
   if (column == 1){
      return wrap("" , "td");
   }
   else{
      return wrap( "" , "td")+makeColumn(column-1);
   }
}

// Generate first row of calendar
function makeHead(){
   // Needed Variables
   var headArray = ['Time', 'Monday', 'Tuesday', 'Wednesday' , 'Thursday' , 'Friday'];
   var i;

   // Return string
   head = "";

   // Create first columns
   for (i=0; i<headArray.length ; i++){
      if (i === 0){
         head = changeClass(head.concat( wrap(headArray[i], "td")) , "time scheduleHead");
      }
      else{
         head = changeClass(head.concat( wrap(headArray[i], "td")) , "scheduleHead");
      }	
   }

   // Wrap to make first row
   head = wrap(head , "tr" , "");

   return head;
}

// Used to change class of schedule table elements
function changeClass(string , aClass){
   return string.replace("defaultClass", aClass);
}

// Used to change id of schedule table elements
function changeId(string , aId){
   return string.replace("defaultId", aId);
}

// from: stackoverflow.com/questions/10073699/pad-a-number-with-leading-zeros-in-javascript
String.prototype.lpad = function(padString, length) {
    var str = this;
    while (str.length < length)
        str = padString + str;
    return str;
}

function normalizeTime(time){
   time = time.split(':');
   time = time[0] + ':' + String(Math.round(time[1]/15)*15).lpad("0",2);
   return time;
}

// Inserts a class into schedule at day with prescribed start and end times
function insertItem( startTime, endTime, day ){
   // Create map from day to column
   var dayToIndex = {"Monday" : 1 , "Tuesday" : 2 , "Wednesday" : 3 , "Thursday" : 4 , "Friday" : 5 };

   // Create map from start time to row
   var startToIndex = {};
   var index = 0;
   $(".time").each(function(){
      if ($(this).text() != "Time"){
         startToIndex[$(this).text()] = index++;
      }
   });

   // Round to nearest 15 minutes:
   startTime = normalizeTime(startTime);
   // Round to nearest 15 minutes:
   endTime = normalizeTime(endTime);


   // Set parameter to remove needed td
   var startRow = startToIndex[startTime]+1;
   var endRow = startToIndex[endTime];
   
   // Hide needed td elements
   for (startRow ; startRow<=endRow ; startRow++){
      $(".scheduleContainer tbody tr:eq("+startRow+") td:eq("+dayToIndex[day]+")").css("display" , "none");
   }

   // Get number of rows needed for new td rowspan
   var nmbrOfRows = startToIndex[endTime] - startToIndex[startTime] + 1;

   // Change rowspan of selected td
   var td = $(".scheduleContainer tbody tr:eq("+startToIndex[startTime]+") td:eq("+dayToIndex[day]+")");
   td.attr("rowspan" , nmbrOfRows);
   td.css("vertical-align", "middle");
   td.css("position" , "relative");

   // Return the td so that we can manipulate it
   return td;
}

function removeItem(startTime , day){

   // Create map from day to column
   var dayToIndex = {"Monday" : 1 , "Tuesday" : 2 , "Wednesday" : 3 , "Thursday" : 4 , "Friday" : 5 };

   // Create map from start time to row
   var startToIndex = {};
   var index = 0;
   $(".time").each(function(){
      if ($(this).text() != "Time"){
         startToIndex[$(this).text()] = index++;
      }
   });

   // Remove display='none' from needed td elements
   var startRow = startToIndex[startTime]+1;
   var endRow = parseInt($(".scheduleContainer tbody tr:eq("+startToIndex[startTime]+") td:eq("+dayToIndex[day]+")").attr("rowspan")) + startRow - 1;

   for (startRow ; startRow<endRow ; startRow++){
      $(".scheduleContainer tbody tr:eq("+startRow+") td:eq("+dayToIndex[day]+")").removeAttr("style");
   }

   // Remove rowspan attribute
   $(".scheduleContainer tbody tr:eq("+startToIndex[startTime]+") td:eq("+dayToIndex[day]+")")
      .removeAttr("rowspan")
      .removeAttr("style")
      .removeClass()
      .addClass("defaultClass")
      .off( "mouseenter mouseleave" )
      .empty(); // clear out the content of the element
}

// Check if specific time slot is available
function available(time , day){

   // Create map from day to column
   var dayToIndex = {"Monday" : 1 , "Tuesday" : 2 , "Wednesday" : 3 , "Thursday" : 4 , "Friday" : 5 };

   // Create map from start time to row
   var startToIndex = {};
   var index = 0;
   $(".time").each(function(){
      if ($(this).text() != "Time"){
         startToIndex[$(this).text()] = index++;
      }
   });

   var displayValue = $(".scheduleContainer tbody tr:eq("+startToIndex[time]+") td:eq("+dayToIndex[day]+")").css("display");
   var rowspanValue = $(".scheduleContainer tbody tr:eq("+startToIndex[time]+") td:eq("+dayToIndex[day]+")").attr("rowspan");

   if ( displayValue != "none" && rowspanValue == undefined){
      return true;
   }

   return false;
}

// Check if all time slots are available
function checkAvailability(startTime , endTime , day){
   startTime = normalizeTime(startTime);
   endTime   = normalizeTime(endTime);
   // If all time slots where available
   if (startTime == increaseTime(endTime)){
      return true;
   }
   // Check if current time slot is available
   if ( available(startTime , day) ){
      // Recursive call , increasing time for next time slot
      return checkAvailability( increaseTime(startTime) , endTime , day);
   }
   else{
      return false;
   }		
}
