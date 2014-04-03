// Create Schedule Table
$( document ).ready(function() {
   var startTime = "8:45";

   $("#calendar thead").append(makeHead())

   $("#calendar tbody").append(makeRows(startTime));

   $.ajax("/register/get-courses",
      {
         dataType:"json",
         success:function(data){
            $.each(data, insertCourse);
         }
      });

});

function insertCourse(i, course){
   console.log(course);
   
   var cssClass          = "sched-group-" + course.course_info.schedule_item_group_id;
   var cssOverBackground = "hsl("+((75*i)%360)+",100%,40%)";
   var cssOutBackground  = "hsl("+((75*i)%360)+",100%,75%)"
   var cssOverColor      = "#FFF";
   var cssOutColor       = "#000";
   var iter_time = function(code){
      return function(j, time){
         var el = insertItem(time.start, time.end, time.day);
         console.log("Inserted: ");
         console.log(el);
         var div = $("<div></div>")
            .css("display", "inline-block")
            .css("position", "relative")
            .css("width", "100%")
            .css("padding", "10px")
            .append("<h3>"+course.course_info.code+"</h3>")
            .append("<p>"+code+"</p>");

         var removeBtn = $("<a>x</a>")
            .css("position","absolute")
            .css("top","10px")
            .css("right","10px");

         div.append(removeBtn);

         el.addClass(cssClass)
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

   if("lec" in course){
      $.each(course.lec.times, iter_time(
               "Lec - " +
               course.lec.section));
   }
   if("tut" in course){
      $.each(course.tut.times, iter_time(
               "Tut - " +
               course.lec.section + " " +
               course.tut.section));
   }
   if("lab" in course){
      $.each(course.lab.times, iter_time(
               "Lab - " +
               course.lec.section + " " +
               course.tut.section + " " +
               course.lab.section));
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
   startTime = startTime.split(':');
   startTime = startTime[0] + ':' + String(Math.round(startTime[1]/15)*15).lpad("0",2);
   // Round to nearest 15 minutes:
   endTime = endTime.split(':');
   endTime = endTime[0] + ':' + String(Math.round(endTime[1]/15)*15).lpad("0",2);


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
