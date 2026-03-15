// chart variable
let chart = null

// form submit event
document
.getElementById("predictionForm")
.addEventListener("submit", function(e){

e.preventDefault()

predictCSAT()

})



async function predictCSAT(){

// loader
const loader = document.getElementById("loader")

loader.classList.remove("hidden")


// get values
const remark = document.getElementById("remark").value.trim()

const response_time = document.getElementById("response_time").value

const survey_delay = document.getElementById("survey_delay").value

const issue_hour = document.getElementById("issue_hour").value

const issue_day = document.getElementById("issue_day").value

const issue_month = document.getElementById("issue_month").value


// validation
if(remark === ""){

alert("Customer remark is required")

loader.classList.add("hidden")

return

}


// request payload
const payload = {

remark: remark,

response_time: response_time,

survey_delay: survey_delay,

issue_hour: issue_hour,

issue_day: issue_day,

issue_month: issue_month

}


try{

// call flask api
const response = await fetch("/predict",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify(payload)

})

const data = await response.json()

loader.classList.add("hidden")


// error check
if(data.error){

document.getElementById("result").innerHTML = data.error

return

}


// show predicted score
document.getElementById("result").innerHTML =
"Predicted CSAT Score : " + data.predicted_csat


// probability data
const probabilities =
data.probabilities.map(p => (p*100).toFixed(2))


const labels =
["CSAT 1","CSAT 2","CSAT 3","CSAT 4","CSAT 5"]


// destroy previous chart
if(chart){

chart.destroy()

}


// create chart
const ctx =
document.getElementById("probChart")
.getContext("2d")


chart = new Chart(ctx,{

type:"bar",

data:{

labels: labels,

datasets:[{

label:"Prediction Confidence (%)",

data: probabilities

}]

},

options:{

responsive:true,

plugins:{

legend:{
display:true
}

},

scales:{

y:{
beginAtZero:true,
max:100
}

}

}

})

}

catch(error){

loader.classList.add("hidden")

document.getElementById("result").innerHTML =
"Prediction failed"

}

}