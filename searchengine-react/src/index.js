import React, {useState} from 'react';
import ReactDOM from "react-dom/client";
import App from "./App";
import './index.css';

const root = ReactDOM.createRoot(document.getElementById("root"));
var searchResult={};

function SearchBar()
{
  const [status,setStatus]=useState(0);

  return (
    <div>
      <h1>Zot Search Engine</h1>
      <div>
        <input type="text" id="query" onKeyPress={(e)=>{
          if(e.key=="Enter")
            document.getElementById("searchBtn").click();
      }}/>
        <button type="button" id="searchBtn" onClick={()=>
        {
          var query=document.getElementById('query').value;
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
      </div>
      <div id="loading" className="noshow"></div>
      <Results results={searchResult}/>
    </div>
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
  console.log(results)
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
      <ResultsHeader/>
      <table>
        <tbody>
        <tr><td>Index</td><td>Result/Timestamp</td><td>URL</td></tr>
        {indexArr.map(i=> (
          <tr className={results[i][3]} key={i}><td>{parseInt(i)+1}</td><td>{results[i][0]}</td><td><a href={results[i][1]}>{results[i][1]}</a></td></tr>
        ))}
        </tbody>
      </table>
    </>
  )
}

function ResultsHeader()
{
  var query=document.getElementById('query').value;
  return
  (
    <h4>Displaying results for "{query}"</h4>
  );
}

function querySearch(query)
{
  return fetch('http://localhost:8000/querySearch/'+query.replace("?","").toLowerCase())
          .then(response => response.json())
          .then(data => data);
}

function filterSelection(c) {
  //console.log("filter "+c);
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
  //console.log("set btn event");
  var current = document.getElementsByClassName("active");
  current[0].className = current[0].className.replace(" active", "");
  e.target.className += " active";
}

root.render(
    <SearchBar />
);
