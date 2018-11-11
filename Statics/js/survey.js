var i=-1;

function add_more(addbtn){
  i++;
  var choices=0;
  var question_label=document.createElement('label');
  question_label.setAttribute('for',i);
  question_label.setAttribute('class',i);
  question_label.setAttribute('id','label' + i);
  var labelVal=i+1;
  question_label.innerHTML="Question "+String(labelVal);
  var question_div=document.createElement('div');
  question_div.setAttribute("id" , i );
  question_div.setAttribute("class" , "q" ,'col-sm-8');
  var delQuestion=document.createElement('button');
  delQuestion.setAttribute("type", "button");
  delQuestion.setAttribute("class", i);
  delQuestion.setAttribute("id", "deleteQuestion" + i);
  delQuestion.setAttribute('onclick','delete_question(this)');
  var delSpan=document.createElement('span');
  delSpan.setAttribute('class','glyphicon glyphicon-remove');
  delSpan.style.color="red";
  delQuestion.appendChild(delSpan);
  var question=document.createElement('input');
  question.setAttribute("type", "text");
  question.setAttribute  ("name","q"+i);
  question.setAttribute("class", "question");
  question.setAttribute("id", "question" + i);
  var br=document.createElement('br');
  var addChoice=document.createElement('button');
  addChoice.setAttribute("type", "button");
  addChoice.setAttribute("onclick","add_choice(this)");
  addChoice.setAttribute("id","addChoice"+ i);
  addChoice.setAttribute("class", i);
  var addSpan=document.createElement('span');
  addSpan.setAttribute('class','glyphicon glyphicon-plus');
  addChoice.appendChild(addSpan);
  document.getElementById('questions').appendChild(question_label);
  document.getElementById('questions').appendChild(question_div);
  document.getElementById(i).appendChild(question);
  document.getElementById(i).appendChild(delQuestion);
  document.getElementById(i).appendChild(br);
  document.getElementById(i).appendChild(addChoice);
  document.getElementById('questions_count').setAttribute('value',i+1);
}

function add_choice(btn){
  var choices=document.getElementById(btn.className).getElementsByTagName('input').length-1;
  var choice=document.createElement('input');
  choice.setAttribute("type", "text");
  choice.setAttribute("name", "item"+ btn.className);
  choice.setAttribute('class','choice');
  choice.setAttribute('id',choices + 'choice'+btn.className);
  var br=document.createElement('br');
  var delBtn=document.createElement('button');
  delBtn.setAttribute('onclick','delete_item(this)');
  delBtn.setAttribute('name','delete'+ btn.className );
  delBtn.setAttribute('id',choices+'deleteItem'+btn.className);
  delBtn.setAttribute('class',btn.className);
  var delSpan=document.createElement('span');
  delSpan.setAttribute('class','glyphicon glyphicon-remove');
  delSpan.style.color="red";
  delBtn.appendChild(delSpan);
  document.getElementById(btn.className).insertBefore(choice,btn);
  document.getElementById(btn.className).insertBefore(delBtn,choice.nextSibling);
  document.getElementById(btn.className).insertBefore(br,btn);

}
function delete_item(btn){
  var deletingElement=btn.previousSibling;
  var thisId=btn.id;
  var start=thisId.slice(0, thisId.indexOf('deleteItem'));
  var idName=btn.parentNode.id;
  var thisClass=btn.className;
  var choices=btn.parentNode.getElementsByTagName('input').length-1;
  document.getElementById(idName).removeChild(deletingElement);
  document.getElementById(idName).removeChild(btn.nextSibling);
  document.getElementById(idName).removeChild(btn);
  for (var a = parseInt(start)+1; a <choices; a++) {
    var pre=a-1;
    document.getElementById(a +'choice'+thisClass).setAttribute('id',pre +'choice'+thisClass)
    document.getElementById(a +'deleteItem'+thisClass).setAttribute('id',pre +'deleteItem'+thisClass)
  }
}
function delete_question(btn){
  var deletingDiv=btn.parentNode;
  var index=parseInt(btn.className)+1;
  document.getElementById('questions').removeChild(deletingDiv.previousSibling);
  document.getElementById('questions').removeChild(deletingDiv);
  for(var a=index;a<=i;a++){
    var pre=a-1;
    var choices=document.getElementById(a).getElementsByTagName('input').length-1;

    for(var b=0;b<choices;b++){
      document.getElementById(b+"choice"+a).setAttribute("name", "item"+ pre);
      document.getElementById(b+"choice"+a).setAttribute("id", b +"choice"+ pre);
      document.getElementById(b+'deleteItem'+a).setAttribute("id", b +"deleteItem"+ pre);
      document.getElementById(b+'deleteItem'+pre).setAttribute("name",'delete'+ pre );
    }
    document.getElementById(a).setAttribute('id',pre);
    document.getElementById("label"+a).innerText="Question"+ a;
    document.getElementById("label"+a).setAttribute('id',"label"+pre);
    document.getElementById("label"+pre).setAttribute('for',pre);
    document.getElementById("question"+a).setAttribute('name',"q"+pre);
    document.getElementById("question"+a).setAttribute('id',"question"+pre);
    document.getElementById("addChoice"+a).setAttribute('class', pre);
    document.getElementById("addChoice"+a).setAttribute('id',"addChoice"+ pre);
    document.getElementById("deleteQuestion"+a).setAttribute('class', pre);
    document.getElementById("deleteQuestion"+a).setAttribute('id',"deleteQuestion"+ pre);

  }
  i--;
  document.getElementById("questions_count").setAttribute("value",i);
}
function getInputsByValue(value)
{
  var allInputs = document.getElementsByTagName("input");
  var results = [];
  for(var x=0;x<allInputs.length;x++)
      if(allInputs[x].value == value)
          results.push(allInputs[x]);
  return results;
}
function insertAfter(newNode, referenceNode) {
referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}
