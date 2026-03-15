async function predictCSAT(){

const remark = document.getElementById("remark").value.trim();
const response_time = document.getElementById("response_time").value;
const survey_delay = document.getElementById("survey_delay").value;
const issue_hour = document.getElementById("issue_hour").value;
const issue_day = document.getElementById("issue_day").value;
const issue_month = document.getElementById("issue_month").value;

const resultDiv = document.getElementById("result");
const loader = document.getElementById("loader");

resultDiv.innerHTML = "";

if(remark === ""){

resultDiv.innerHTML = "Please enter customer remark";
return;

}

const payload = {

remark: remark,
response_time: response_time,
survey_delay: survey_delay,
issue_hour: issue_hour,
issue_day: issue_day,
issue_month: issue_month

};

loader.classList.remove("hidden");

try{

const response = await fetch("/predict",{

method:"POST",
headers:{
"Content-Type":"application/json"
},

body:JSON.stringify(payload)

});

const data = await response.json();

loader.classList.add("hidden");

if(data.error){

resultDiv.innerHTML = data.error;
return;

}

resultDiv.innerHTML = "Predicted CSAT Score : " + data.predicted_csat;

}

catch(error){

loader.classList.add("hidden");

resultDiv.innerHTML = "Prediction failed";

}

}