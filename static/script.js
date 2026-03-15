let chart = null

async function predictCSAT(){

// get inputs
const remark = document.getElementById("remark").value

const response_time = document.getElementById("response_time").value

const survey_delay = document.getElementById("survey_delay").value

const issue_hour = document.getElementById("issue_hour").value

const issue_day = document.getElementById("issue_day").value

const issue_month = document.getElementById("issue_month").value


// create payload
const payload = {

remark: remark,

response_time: response_time,

survey_delay: survey_delay,

issue_hour: issue_hour,

issue_day: issue_day,

issue_month: issue_month

}


// call flask api
const response = await fetch("/predict",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify(payload)

})

const data = await response.json()


// show predicted csat
document.getElementById("result").innerHTML =
"Predicted CSAT Score : " + data.predicted_csat


// get probabilities
const probs = data.probabilities.map(p => (p*100).toFixed(2))


// chart labels
const labels = ["CSAT 1","CSAT 2","CSAT 3","CSAT 4","CSAT 5"]


// destroy old chart
if(chart){

chart.destroy()

}


// create chart
const ctx = document.getElementById("probChart").getContext("2d")

chart = new Chart(ctx,{

type:"bar",

data:{

labels: labels,

datasets:[{

label:"Prediction Confidence (%)",

data: probs

}]

},

options:{

scales:{

y:{

beginAtZero:true,

max:100

}

}

}

})

}