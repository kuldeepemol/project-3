function init() {
  // Grab a reference to the dropdown select element
  var dirSelector = d3.select("#selDirector");

  // Use the list of director-names to populate the select options
  d3.json("/directors").then((directorNames) => {
    directorNames.forEach((director) => {
      dirSelector
        .append("option")
        .text(director.name)
        .property("value", director.value);
    });

  });

  // Grab a reference to the dropdown select element
  var actorSelector1 = d3.select("#selActor1");

  // Use the list of director-names to populate the select options
  d3.json("/actors_1").then((Actors) => {
    Actors.forEach((actor) => {
      actorSelector1
        .append("option")
        .text(actor.name)
        .property("value", actor.value);
    });

  });

  // Grab a reference to the dropdown select element
  var actorSelector2 = d3.select("#selActor2");

  // Use the list of director-names to populate the select options
  d3.json("/actors_2").then((Actors) => {
    Actors.forEach((actor) => {
      actorSelector2
        .append("option")
        .text(actor.name)
        .property("value", actor.value);
    });

  });

  // Grab a reference to the dropdown select element
  var actorSelector3 = d3.select("#selActor3");

  // Use the list of director-names to populate the select options
  d3.json("/actors_3").then((Actors) => {
    Actors.forEach((actor) => {
      actorSelector3
        .append("option")
        .text(actor.name)
        .property("value", actor.value);
    });

  });

  // Grab a reference to the dropdown select element
  var crSelector = d3.select("#selCR");

  // Use the list of director-names to populate the select options
  d3.json("/ratings").then((Names) => {
    Names.forEach((name) => {
      crSelector
        .append("option")
        .text(name)
        .property("value", name);
    });

  });
}

var predictBtnObj = d3.select('#buttonPredict');
predictBtnObj.on('click', function() {

    // Prevent the page from refreshing
    d3.event.preventDefault();

    var finalPredictMsg = d3.select('#finalPredictMsg');
    finalPredictMsg.html('');
    finalPredictMsg.style('display', 'none');
    finalPredictMsg.attr("class", "");

    var url = '/predict/'
     // Get all select elements
    var allSelect = d3.selectAll('select');
    allSelect.nodes().forEach(eachSelect => {
        var selectId = eachSelect.id;
        var selectValue = eachSelect.value;
        //alert(selectId+" ==> "+selectValue);
        url = url + selectValue + '/';
    });

    // Get all Input elements
    var inputBudget = d3.select('#inputBudget');
    var budgetValue = inputBudget.property('value');
    if (budgetValue) {
        url = url + budgetValue;
    } else {
        alert('Please enter budget value, for better prediction.')
        return false;
    }

    d3.json(url).then((data) => {
        finalPredictMsg.html("<strong>"+data.final_predict_message+"</strong>");
        finalPredictMsg.style('display', 'block');
        if (data.final_predict_category == 1) {
            finalPredictMsg.attr("class", "alert alert-danger");
        } else if (data.final_predict_category == 2) {
            finalPredictMsg.attr("class", "alert alert-info");
        } else if (data.final_predict_category == 3) {
            finalPredictMsg.attr("class", "alert alert-success");
        } else if (data.final_predict_category == 4) {
            finalPredictMsg.attr("class", "alert alert-success");
        }
    });
});


// Initialize
init();

