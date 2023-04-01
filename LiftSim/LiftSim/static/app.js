const {Input} = require('./Dynamic Input');

var now_value1=1;//Current Floor for Lift 1
var now_value2=1;//Current Floor for Lift 2
var now_value3=1;//Current Floor for Lift 3
var plan_value1=now_value1;//Lift 1 initial plan Floor to stop
var plan_value2=now_value2;//Lift 2 initial plan Floor to stop
var plan_value3=now_value3;//Lift 3 initial plan Floor to stop
var Floor_status1=0;//Current Status for Lift 1, Stop
var Floor_status2=0;//Current Status for Lift 2, Stop
var Floor_status3=0;//Current Status for Lift 3, Stop
var Floor_num=9;
var Floor_plan1=new Array();
var Floor_plan2=new Array();
var Floor_plan3=new Array();


// 电梯模拟运行，Write by Showlin (fzsalx@163.com)-->
 function SetLight(num, lift){ //点亮某层的灯
  var obj;
  var tmpstring;
   tmpstring="Submit" + num.toString() + "_" + lift.toString();
   obj=document.getElementById(tmpstring);
    document.getElementById("now_position_" + lift).innerText=window["now_value" + lift];
    obj.style.background="#ffff00";
 }

 function SetUnLight(num, lift){ //熄灭某层的灯
  var obj;
  var tmpstring;
   tmpstring="Submit" + num.toString() + "_" + lift.toString();
   obj=document.getElementById(tmpstring);
   obj.style.background="#d4d0c8";
 }
 
 function SetRed(num, lift){//到达提示
  var obj;
  var tmpstring;
   tmpstring="Submit" + num.toString()+ "_" + lift;
   obj=document.getElementById(tmpstring);
   obj.style.background="#ff0000";
 }
 
 function goto(obj,lift){//按按钮之后
  var i;
  var tmpobj;
  var tmpstring;
  var tmpvalue;
  tmpvalue=parseInt(obj.value);
  SetIsPlan(tmpvalue,lift);  //点亮按下的楼层灯
  if (tmpvalue==window["now_value" + lift]) return; //终点和起点一致不控制
  if (window["Floor_status" + lift]==0){
   window["plan_value" + lift]=tmpvalue;//设置电梯初始运行终点
   if (window["plan_value" + lift]>window["now_value" + lift]){//上行
    window["Floor_status" + lift]=1;
    up(lift);
   }else{
    window["Floor_status" + lift]=-1;
    down(lift);
   }
  }else{
   AddPlan(obj.value,lift);//添加到计划停靠表中等待
  }
  
 }
 
 function up(lift){//上行
  SetUnLight(window["now_value" + lift],lift);//设置离开的楼层显示状态
  window["now_value" + lift]++;//上行
  SetLight(window["now_value" + lift],lift);//顶端显示状态
  if (window["Floor_plan" + lift].length==0) {//计划停靠表为空
   if (window["plan_value" + lift]!=window["now_value" + lift]) {//若未抵达延时继续上行
    setTimeout(up,1000,lift);
   }else{
    DelAll(lift);//所有灯灭；
    SetLight(window["now_value" + lift],lift);
    window["Floor_status" + lift]=0;//设置电梯为停
   }
  }else{
   if (window["Floor_plan" + lift][window["Floor_plan" + lift].length-1]==window["now_value" + lift]){ //判断是否到了下一个停靠点
    SetRed(window["now_value" + lift],lift);//设置停靠点状态
    DelPlan(lift);//删除最后一个停靠点的信息
    if (window["Floor_plan" + lift].length==0){//判断停靠计划表是否为空
     DelAll(lift);//所有灯灭；
     SetLight(window["now_value" + lift],lift);
     window["Floor_status" + lift]=0;//停
    }else{
     setTimeout(up,2000,lift);//继续
    }
   }else{//没到下一个停靠点
     setTimeout(up,1000,lift);   
   }
  }
 }
 
 function down(lift){//下行
  SetUnLight(window["now_value" + lift],lift);//设置离开的楼层显示状态
  window["now_value" + lift]--;//下行
  SetLight(window["now_value" + lift],lift);//顶端显示状态
  if (window["Floor_plan" + lift].length==0) {//计划停靠表为空
   if (window["plan_value" + lift]!=window["now_value" + lift]) {//若未抵达延时继续上行
    setTimeout("down(lift)",1000);
   }else{
    DelAll(lift);//所有灯灭；
    SetLight(window["now_value" + lift],lift);
    window["Floor_status" + lift]=0;//设置电梯为停
   }
  }else{
   if (window["Floor_plan" + lift][window["Floor_plan" + lift].length-1]==window["now_value" + lift]){ //判断是否到了下一个停靠点
    SetRed(window["now_value" + lift],lift);//设置停靠点状态
    DelPlan(lift);//删除最后一个停靠点的信息
    if (window["Floor_plan" + lift].length==0){//判断停靠计划表是否为空
     DelAll(lift);//所有灯灭；
     SetLight(window["now_value" + lift],lift);
     window["Floor_status" + lift]=0;//停
    }else{
     setTimeout("down(lift)",2000);//继续
    }
   }else{//没到下一个停靠点
     setTimeout("down(lift)",1000);   
   }
  }
 }
 function AddPlan(num, lift){//添加计划停靠表
  if (window["Floor_status" + lift]*num<window["now_value" + lift]*window["Floor_status" + lift]) return;//按钮与电梯方向相反则不予理会
  if (window["Floor_plan" + lift].length==0){//计划表为空
   if (window["Floor_status" + lift]*num>window["plan_value" + lift]*window["Floor_status" + lift]){
    window["Floor_plan" + lift][0]=num;
    window["Floor_plan" + lift][1]=window["plan_value" + lift];
   }
   if (window["Floor_status" + lift]*num<window["plan_value" + lift]*window["Floor_status" + lift]){
    window["Floor_plan" + lift][1]=num;
    window["Floor_plan" + lift][0]=window["plan_value" + lift];
   }
  }else{
   var i;
   var j;
   for (i=0;i<window["Floor_plan" + lift].length;i++){
    if (num==window["Floor_plan" + lift][i]) return;
    if (window["Floor_status" + lift]*num>window["Floor_plan" + lift][i]*window["Floor_status" + lift]){//找出插入的位置
     for (j=window["Floor_plan" + lift].length;j>i;j--) {window["Floor_plan" + lift][j]=window["Floor_plan" + lift][j-1];}
     window["Floor_plan" + lift][i]=num;
     break;
    }
   }
   if (i==window["Floor_plan" + lift].length) window["Floor_status" + lift][i]=num; //插入到数组尾部
  }

 }
 
 function DelPlan(lift){//去除计划表最后一项，停靠点
  window["Floor_plan" + lift].length--;
 }
 
 
 function SetIsPlan(num,lift){//设置按下按钮的灯
  var obj;
  var tmpstring;
   tmpstring="Submit" + num.toString() + "_" + lift.toString();
   obj=document.getElementById(tmpstring);
   obj.style.background="#66ffff";
 }

 function DelAll(lift){//熄灭所有灯
  var i=1
  for (i=1;i<=Floor_num;i++)  SetUnLight(i,lift);
 }



 


 function addPassenger() {
  const numOfPeople = parseInt(document.getElementById("numOfPeople").value);
  const sourceFloor = parseInt(document.getElementById("sourceFloor").value);
  const destinationFloor = parseInt(document.getElementById("destinationFloor").value);
  
  // Validate input
  if (numOfPeople <= 0 || sourceFloor < 1 || sourceFloor > 10 || destinationFloor < 1 || destinationFloor > 10) {
    alert("Please enter valid input.");
    return;
  }
  
  // Add passenger to list
  passengers.push({
    numOfPeople: numOfPeople,
    sourceFloor: sourceFloor,
    destinationFloor: destinationFloor
  });
  
  // Add passenger to lift queue
  addPassengerToQueue(numOfPeople, sourceFloor, destinationFloor);
  
  // Clear input fields
  document.getElementById("numOfPeople").value = "";
  document.getElementById("sourceFloor").value = "";
  document.getElementById("destinationFloor").value = "";
}

