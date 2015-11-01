1. USE es5_shim.min.js to handle js compatible (new added)
2. use htm5shiv to adjust html related fix  
3. use respond.proxy.js(production) and respond.min.js(testing) to hanlde css media query

4. a bug , happen in IE8 , in serverSide. 

   guoku's JSONResponse class : in (app/core/utils/http)
   
   default response with a header with content_type='application/json; charset=utf8'
   
   this will cause IE8's xhr object emmit "error c00ce56e"
   
   IE8 can not parse unidentified charset , 
   ====================================
   fix : must change it to utf-8 ,
   
5. more bug , happen in IE8 , in js file ,

   some code in site.js iterate a array with following code
   
   for(var j in someArray){.......}
   
   in IE8 , this will cause error ,
   because j will iterate with value of Array's property like "slice" !!!
   
   use another form of iteration method like following 
   
   for (var i=0 , len=someArray.length; i< len; i++){.....}
   
   
  