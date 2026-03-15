async function predictCSAT(){

// get input values
const remark = document.getElementById("remark").value

const response_time = document.getElementById("response_time").value

const survey_delay = document.getElementById("survey_delay").value

const issue_hour = document.getElementById("issue_hour").value

const issue_day = document.getElementById("issue_day").value

const issue_month = document.getElementById("issue_month").value


const payload = {

remark: remark,

response_time: response_time,

survey_delay: survey_delay,

issue_hour: issue_hour,

issue_day: issue_day,

issue_month: issue_month

}


const response = await fetch("/predict",{

method:"POST",

headers:{

"Content-Type":"application/json"

},

body:JSON.stringify(payload)

})


const data = await response.json()


// show predicted CSAT
document.getElementById("result").innerHTML =

"Predicted CSAT Score : " + data.predicted_csat


// show probabilities
let prob_html = "<h3>Confidence</h3>"


for(let i=0;i<data.probabilities.length;i++){

let percent = (data.probabilities[i]*100).toFixed(2)

prob_html += "CSAT " + (i+1) + " : " + percent + "%<br>"

}


document.getElementById("probabilities").innerHTML = prob_html

}