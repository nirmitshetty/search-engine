import React, {useState} from 'react';
import ReactDOM from "react-dom/client";
import App from "./App";
import './index.css';

const root = ReactDOM.createRoot(document.getElementById("root"));
var searchResult={};

function querySearch(query)
{
  var option=3;
  return fetch('http://localhost:8000/querySearch/'+query.replace("?","").toLowerCase()+'/'+option)
          .then(response => response.json())
          .then(data => data);
}

function Header()
{
  const [status,setStatus]=useState(0);

  return (
    <div>
      <h1>Zot Search Engine</h1>
      <div>
        <input type="text" id="query"/>
        <button type="button" onClick={()=>
        {
          var query=document.getElementById('query').value;
          console.log('initiating hit');
          querySearch(query).then(res=>
            {
              if(typeof res == "string")
                searchResult=JSON.parse(res);
              else
                searchResult=res;
              setStatus(status+1);
            });
        }}>Search</button>
      </div>

      <Results results={searchResult} />
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
      <table>
        <tbody>
        <tr><td>Index</td><td>Result/Timestamp</td><td>URL</td></tr>
        {indexArr.map(i=> (
          <tr key={i}><td>{parseInt(i)+1}</td><td>{results[i][0]}</td><td><a href={results[i][1]}>{results[i][1]}</a></td></tr>
        ))}
        </tbody>
      </table>
    </>
  )
}

root.render(
    <Header />
);
