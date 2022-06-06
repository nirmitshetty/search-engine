import React, {useState,useEffect} from 'react';
import ReactDOM from "react-dom/client";
import App from "./App";
import './index.css';

const root = ReactDOM.createRoot(document.getElementById("root"));
var searchResult={};

var startTime, endTime;

function SearchBar()
{
  const [status,setStatus]=useState(0);

  useEffect(()=>{

    fetch('http://localhost:8000/getQuestions/')
            .then(response => response.json())
            .then(data => {

              autocomplete(document.getElementById('query'),data);
            });
}, [])

  return (
    <section>

      <div className="main">

        <img src={require("./zotsearch.png")} height="100" />

        <div className="autocomplete" >
          <input type="text" className="searchBox" id="query" placeholder="type your query" />
          <button className="searchButton" type="button" id="searchBtn" onClick={()=>
          {
            start();
            var query=document.getElementById('query').value;
            if(query=="")
              return;
            var loader=document.getElementById('loading');
            loader.className="loader";
            console.log('initiating hit');
            querySearch(query).then(res=>
              {
                loader.className="noshow";
                if(typeof res == "string")
                  searchResult=JSON.parse(res);
                else
                  searchResult=res;
                setStatus(status+1);
              });
          }}>Search</button>
          <div className='icon'>
            <img src={require("./search_icon.png")} />
          </div>

        </div>

        <div id="loading" className="noshow"></div>
        <Results results={searchResult}/>
      </div>
    </section>
  );
}

function Filters()
{
  return(
    <div id="myBtnContainer">
      <button className="btn active" onClick={(e)=>
        {
          filterSelection('all');
          setActiveBtnEvent(e);
        }}>All Results</button>
      <button className="btn" onClick={(e)=>{
        filterSelection('text')
        setActiveBtnEvent(e);
      }}>Web pages</button>
      <button className="btn" onClick={(e)=>{
        filterSelection('video')
        setActiveBtnEvent(e);
      }}>Videos</button>
    </div>
  );
}

function Results({results})
{
  //console.log(results)
  var indexArr=[];
  if(Object.keys(results).length!=0)
  {
    indexArr=Object.keys(results);
  }
  else {
      return;
  }

  return(
    <>
      <Filters/>
      <table>
        <tbody>
          <tr ><td ><p className="resultHeading">Displaying results for <span className="highlight">&nbsp;{document.getElementById('query').value}&nbsp;</span> ({end()} seconds)</p></td></tr>
          {indexArr.map(i=> <ResultRow result={results[i]} index={i}/>)}
        </tbody>
      </table>
    </>
  )
}

function ResultRow(props)
{
  var result=props.result;
  var index=props.index;
  if(result[4]=="text")
  {
    return(
      <tr className="text" key={index}>
        <td>
          <p className='title'><a href={result[1]} target="_blank">{result[3]}</a></p>
          <p className='url'><a href={result[1]} target="_blank">{result[1]}</a></p>
          <p className='answer'>{result[0]}</p>
        </td>
      </tr>);
  }
  else
  {
    var id=result[1].split("=")[1];
    var timestamp=result[0].split(":");
    timestamp=parseInt(timestamp[0])*60+parseInt(timestamp[1]);
    var embed=result[1].replace("watch?v=","embed/")

    return(
      <tr className="video" key={index}>
        <td>
          <div className="videoContainer">
            <div><iframe src={embed+"?start="+timestamp} allowFullScreen="allowFullScreen" frameBorder="0"/></div>
            <div className="videoText">
              <p className='title'><a href={result[1]+"&start="+timestamp} target="_blank">{result[2]}</a></p>
              <p className='answer'>{result[3]}</p>
            </div>
          </div>
        </td>
      </tr>);
  }
}

function querySearch(query)
{
  return fetch('http://localhost:8000/querySearch/'+query.replace("?","").toLowerCase())
          .then(response => response.json())
          .then(data => data);
}

function filterSelection(c) {

  var x1,x2, i,o1,o2;
  x1= document.getElementsByClassName("text");
  x2 = document.getElementsByClassName("video");
  o1=" noshow";
  o2=" noshow";

  if (c == "all" || c=="text")
    o1=""
  if (c == "all" || c=="video")
      o2=""

  for (i = 0; i < x1.length; i++)
    x1[i].className="text"+o1;

  for (i = 0; i < x2.length; i++)
    x2[i].className="video"+o2;
}

function setActiveBtnEvent(e)
{

  var current = document.getElementsByClassName("active");
  current[0].className = current[0].className.replace(" active", "");
  e.target.className += " active";
}

function autocomplete(inp,arr) {

  /*the autocomplete function takes two arguments,
  the text field element and an array of possible autocompleted values:*/
  var currentFocus;
  /*execute a function when someone writes in the text field:*/
  inp.addEventListener("input", function(e) {

      var a, b, i, count, val = this.value;
      /*close any already open lists of autocompleted values*/
      closeAllLists();
      if (!val) { return false;}
      currentFocus = -1;
      /*create a DIV element that will contain the items (values):*/
      a = document.createElement("DIV");
      a.setAttribute("id", this.id + "autocomplete-list");
      a.setAttribute("class", "autocomplete-items");
      /*append the DIV element as a child of the autocomplete container:*/

      this.parentNode.appendChild(a);
      /*for each item in the array...*/
      for (i = 0,count=0; i < arr.length && count<10; i++) {
        /*check if the item starts with the same letters as the text field value:*/
        //if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
        if(arr[i].toLowerCase().includes(val.toLowerCase())){
          count++;
          /*create a DIV element for each matching element:*/
          b = document.createElement("DIV");
          /*make the matching letters bold:*/
          b.innerHTML = arr[i].substr(0);

          /*insert a input field that will hold the current array item's value:*/
          b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
          /*execute a function when someone clicks on the item value (DIV element):*/
          b.addEventListener("click", function(e) {
              /*insert the value for the autocomplete text field:*/
              inp.value = this.getElementsByTagName("input")[0].value;
              /*close the list of autocompleted values,
              (or any other open lists of autocompleted values:*/
              closeAllLists();
          });
          a.appendChild(b);
        }
      }
  });
  /*execute a function presses a key on the keyboard:*/
  inp.addEventListener("keydown", function(e) {
      var x = document.getElementById(this.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.keyCode == 40) {
        /*If the arrow DOWN key is pressed,
        increase the currentFocus variable:*/
        currentFocus++;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 38) { //up
        /*If the arrow UP key is pressed,
        decrease the currentFocus variable:*/
        currentFocus--;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 13) {
        /*If the ENTER key is pressed, prevent the form from being submitted,*/
        //e.preventDefault();
        if (currentFocus > -1) {
          /*and simulate a click on the "active" item:*/
          if (x) x[currentFocus].click();
        }
        document.getElementById("searchBtn").click();
      }
  });
  function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("autocomplete-active");
  }
  function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }
  function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
        x[i].parentNode.removeChild(x[i]);
      }
    }
  }
  /*execute a function when someone clicks in the document:*/
  document.addEventListener("click", function (e) {
      closeAllLists(e.target);
  });
}

function start() {
  startTime = new Date();
};

function end() {
  endTime = new Date();
  var timeDiff = endTime - startTime; //in ms
  // strip the ms
  timeDiff /= 1000;

  // get seconds
  //var seconds = Math.round(timeDiff);
  return timeDiff;
}

root.render(
    <SearchBar />
);
