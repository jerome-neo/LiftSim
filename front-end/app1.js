var now_value=1;//电梯当前楼层
var plan_value=now_value;//电梯初始计划停靠楼层
var Floor_status=0;//电梯当前状态，停
var Floor_num=9;
var Floor_plan=new Array();

/*var now_value2=1;//电梯当前楼层
var plan_value2=now_value2;//电梯初始计划停靠楼层
var Floor_status2=0;//电梯当前状态，停
var Floor_num2=9;
var Floor_plan2=new Array();

var now_value3=1;//电梯当前楼层
var plan_value3=now_value3;//电梯初始计划停靠楼层
var Floor_status3=0;//电梯当前状态，停
var Floor_num3=9;
var Floor_plan3=new Array();*/

// 电梯模拟运行，Write by Showlin (fzsalx@163.com)-->
 function SetLight1(num){ //点亮某层的灯
  var obj;
  var tmpstring;
   tmpstring="Submit" + num.toString();
   obj=document.getElementById(tmpstring);
    document.getElementById("now_position").innerText=now_value1;
    obj.style.background="#ffff00";
 }

 function SetLight2(num){ //点亮某层的灯
  var obj;
  var tmpstring;
   tmpstring="Submit" + num.toString();
   obj=document.getElementById(tmpstring);
    document.getElementById("now_position").innerText=now_value2;
    obj.style.background="#ffff00";
 }

 function SetLight3(num){ //点亮某层的灯
  var obj;
  var tmpstring;
   tmpstring="Submit" + num.toString();
   obj=document.getElementById(tmpstring);
    document.getElementById("now_position").innerText=now_value3;
    obj.style.background="#ffff00";
 }

 function SetUnLight1(num){ //熄灭某层的灯
  var obj;
  var tmpstring;
   tmpstring="Submit" + num.toString();
   obj=document.getElementById(tmpstring);
   obj.style.background="#d4d0c8";
 }
 
 function SetUnLight2(num){ //熄灭某层的灯
  var obj;
  var tmpstring;
   tmpstring="Submit" + num.toString();
   obj=document.getElementById(tmpstring);
   obj.style.background="#d4d0c8";
 }

 function SetUnLight3(num){ //熄灭某层的灯
  var obj;
  var tmpstring;
   tmpstring="Submit" + num.toString();
   obj=document.getElementById(tmpstring);
   obj.style.background="#d4d0c8";
 }

 function SetRed1(num){//到达提示
  var obj;
  var tmpstring;
   tmpstring="Submit" + num.toString();
   obj=document.getElementById(tmpstring);
   obj.style.background="#ff0000";
 }

 function SetRed2(num){//到达提示
  var obj;
  var tmpstring;
   tmpstring="Submit" + num.toString();
   obj=document.getElementById(tmpstring);
   obj.style.background="#ff0000";
 }
 
 function SetRed3(num){//到达提示
  var obj;
  var tmpstring;
   tmpstring="Submit" + num.toString();
   obj=document.getElementById(tmpstring);
   obj.style.background="#ff0000";
 }

 function goto1(obj){//按按钮之后
  var i;
  var tmpobj;
  var tmpstring;
  var tmpvalue;
  tmpvalue=parseInt(obj.value);
  SetIsPlan1(tmpvalue);  //点亮按下的楼层灯
  if (tmpvalue==now_value1) return; //终点和起点一致不控制
  if (Floor_status1==0){
   plan_value1=tmpvalue;//设置电梯初始运行终点
   if (plan_value1>now_value1){//上行
    Floor_status1=1;
    up();
   }else{
    Floor_status1=-1;
    down();
   }
  }else{
   AddPlan(obj.value);//添加到计划停靠表中等待
  }
  
 }

 function goto2(obj){//按按钮之后
  var i;
  var tmpobj;
  var tmpstring;
  var tmpvalue;
  tmpvalue=parseInt(obj.value);
  SetIsPlan(tmpvalue);  //点亮按下的楼层灯
  if (tmpvalue==now_value2) return; //终点和起点一致不控制
  if (Floor_status2==0){
   plan_value2=tmpvalue;//设置电梯初始运行终点
   if (plan_value2>now_value2){//上行
    Floor_status2=1;
    up();
   }else{
    Floor_status2=-1;
    down();
   }
  }else{
   AddPlan(obj.value);//添加到计划停靠表中等待
  }
  
 }

 function goto3(obj){//按按钮之后
  var i;
  var tmpobj;
  var tmpstring;
  var tmpvalue;
  tmpvalue=parseInt(obj.value);
  SetIsPlan(tmpvalue);  //点亮按下的楼层灯
  if (tmpvalue==now_value3) return; //终点和起点一致不控制
  if (Floor_status3==0){
   plan_value3=tmpvalue;//设置电梯初始运行终点
   if (plan_value3>now_value3){//上行
    Floor_status3=1;
    up();
   }else{
    Floor_status3=-1;
    down();
   }
  }else{
   AddPlan(obj.value);//添加到计划停靠表中等待
  }
  
 }
 
 function up(){//上行
  SetUnLight(now_value);//设置离开的楼层显示状态
  now_value++;//上行
  SetLight(now_value);//顶端显示状态
  if (Floor_plan.length==0) {//计划停靠表为空
   if (plan_value!=now_value) {//若未抵达延时继续上行
    setTimeout("up()",1000);
   }else{
    DelAll();//所有灯灭；
    SetLight(now_value);
    Floor_status=0;//设置电梯为停
   }
  }else{
   if (Floor_plan[Floor_plan.length-1]==now_value){ //判断是否到了下一个停靠点
    SetRed(now_value);//设置停靠点状态
    DelPlan();//删除最后一个停靠点的信息
    if (Floor_plan.length==0){//判断停靠计划表是否为空
     DelAll();//所有灯灭；
     SetLight(now_value);
     Floor_status=0;//停
    }else{
     setTimeout("up()",2000);//继续
    }
   }else{//没到下一个停靠点
     setTimeout("up()",1000);   
   }
  }
 }
 
 function down(){//下行
  SetUnLight(now_value);//设置离开的楼层显示状态
  now_value--;//下行
  SetLight(now_value);//顶端显示状态
  if (Floor_plan.length==0) {//计划停靠表为空
   if (plan_value!=now_value) {//若未抵达延时继续上行
    setTimeout("down()",1000);
   }else{
    DelAll();//所有灯灭；
    SetLight(now_value);
    Floor_status=0;//设置电梯为停
   }
  }else{
   if (Floor_plan[Floor_plan.length-1]==now_value){ //判断是否到了下一个停靠点
    SetRed(now_value);//设置停靠点状态
    DelPlan();//删除最后一个停靠点的信息
    if (Floor_plan.length==0){//判断停靠计划表是否为空
     DelAll();//所有灯灭；
     SetLight(now_value);
     Floor_status=0;//停
    }else{
     setTimeout("down()",2000);//继续
    }
   }else{//没到下一个停靠点
     setTimeout("down()",1000);   
   }
  }
 }
 function AddPlan(num){//添加计划停靠表
  if (Floor_status*num<now_value*Floor_status) return;//按钮与电梯方向相反则不予理会
  if (Floor_plan.length==0){//计划表为空
   if (Floor_status*num>plan_value*Floor_status){
    Floor_plan[0]=num;
    Floor_plan[1]=plan_value;
   }
   if (Floor_status*num<plan_value*Floor_status){
    Floor_plan[1]=num;
    Floor_plan[0]=plan_value;
   }
  }else{
   var i;
   var j;
   for (i=0;i<Floor_plan.length;i++){
    if (num==Floor_plan[i]) return;
    if (Floor_status*num>Floor_plan[i]*Floor_status){//找出插入的位置
     for (j=Floor_plan.length;j>i;j--) {Floor_plan[j]=Floor_plan[j-1];}
     Floor_plan[i]=num;
     break;
    }
   }
   if (i==Floor_plan.length) Floor_plan[i]=num; //插入到数组尾部
  }

 }
 
 function DelPlan(){//去除计划表最后一项，停靠点
  Floor_plan.length--;
 }
 
 
 function SetIsPlan(num){//设置按下按钮的灯
  var obj;
  var tmpstring;
   tmpstring="Submit" + num.toString();
   obj=document.getElementById(tmpstring);
   obj.style.background="#66ffff";
 }

 function DelAll(){//熄灭所有灯
  var i=1
  for (i=1;i<=Floor_num;i++)  SetUnLight(i);
 }

 