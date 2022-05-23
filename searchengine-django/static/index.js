function search()
{
  payload=document.getElementById('query').value;

  $.ajax({
    type: "GET",
    url: "http://localhost:8000/querySearch/"+payload,
    /*
    success: function(res) {

      console.log(JSON.parse(res));

    }
    */
  });

  //console.log("button clicked end");
}