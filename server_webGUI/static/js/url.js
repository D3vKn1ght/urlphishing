Pusher.logToConsole = true;

// Configure Pusher instance
var pusher = new Pusher('e0f057db90b68cb7a529', {
  cluster: 'ap1',
  encrypted: true
});



var customerChannel = pusher.subscribe('url');
customerChannel.bind('add_1', function(data) {
var date = new Date();

console.log(".1-url")
$(".statistic_tb-bd").append(
    "<tr>" +
    "<td>" +  data.url + "</td>" +
    "<td>" + `${date.getFullYear()}/${date.getMonth()}/${date.getDay()}  ${date.getHours()}:${date.getMinutes()}:${date.getSeconds()} ` + "</td>" +
    "<td class='tb-detect-result'>" + data.type + "</td>" +
    "</tr>"
)


var dt_result = $(".tb-detect-result");
Array.from(dt_result).forEach(element => {
    console.log(element.outerText);
    switch (element.outerText) {
        case "UNSAFE":
            element.style.color = "#000";
            element.style.backgroundColor = "red"
            console.log("red")
            break;
        case "SAFE":
            element.style.color = "#000";
            element.style.backgroundColor = "#198754";
            break;
        case "SUSPICIOUS":
            element.style.color = "#000";
            element.style.backgroundColor = "#ffc107";
            break;
        default:
            console.log("error");
            break;
    }
})
})