//Document is the DOM can be accessed in the console with document.window.
// Tree is from the top, html, body, p etc.


//Event handling, uder interaction is what starts the code execution.

var taskInput=document.getElementById("new-task");//Add a new task.
var addButton=document.getElementById("add");//first button
console.log("add button")
var incompleteTaskHolder=document.getElementById("incomplete-tasks");//ul of #incomplete-tasks
var completedTasksHolder=document.getElementById("completed-tasks");//completed-tasks

var csrfToken = document.cookie.match(/csrftoken=([\w-]+)/)[1];


//New task list item
var createNewTaskElement=function(taskString, taskId){
    console.log('we create')

	var listItem=document.createElement("li");

	listItem.setAttribute("data-id", taskId);

	//input (checkbox)
	var checkBox=document.createElement("input");//checkbx
	//label
	var label=document.createElement("label");//label
	//input (text)
	var editInput=document.createElement("input");//text
	editInput.style.display='none';
	//button.edit
	var editButton=document.createElement("button");//edit button

	//button.delete
	var deleteButton=document.createElement("button");//delete button

	label.innerText=taskString;

	//Each elements, needs appending
	checkBox.type="checkbox";
	editInput.type="text";
	editInput.className="todo";


	editButton.innerText="Edit";//innerText encodes special characters, HTML does not.
	editButton.className="edit todo";
	deleteButton.innerText="Delete";
	deleteButton.className="delete todo";


	//and appending.
	listItem.appendChild(checkBox);
	listItem.appendChild(label);
	listItem.appendChild(editInput);
	listItem.appendChild(editButton);
	listItem.appendChild(deleteButton);
	return listItem;
}


var addTask = function() {
    console.log("Add Task...");
    var taskData = {
        name: taskInput.value,
        state: 'incomplete'
    };
    fetch('/moneitas/api/create_task/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(taskData)
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();  // Si esperas una respuesta en JSON
    })
    .then(data => {
        console.log('Tarea creada:', data);
        var listItem = createNewTaskElement(data.name, data.id);
        incompleteTaskHolder.appendChild(listItem);
        bindTaskEvents(listItem, taskCompleted);
    })
    .catch(error => console.error('Error:', error));

    taskInput.value = '';
}

//Edit an existing task.
var editTaskname=function(){
    console.log("Edit Task Name...");
    console.log("Change 'edit' to 'save'");

    var listItem=this.parentNode;
    var editInput=listItem.querySelector('input[type=text]');
    var label=listItem.querySelector("label");
    var containsClass=listItem.classList.contains("editMode");
    var taskId = listItem.getAttribute('data-id');
    var taskData = {
        name: editInput.value,
    };
    if(containsClass){
        editTask(taskData, taskId);
        label.innerText=editInput.value;
        editInput.style.display = 'none';
    }else{
    	editInput.value=label.innerText;
    	editInput.style.display = 'block';
    }
    //toggle .editmode on the parent.
    listItem.classList.toggle("editMode");
}

var editTask=function(jsonDict, taskId){

    fetch(`/moneitas/api/edit_task/${taskId}/`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(jsonDict)
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();  // Si esperas una respuesta en JSON
    })
    .then(data => {
        console.log('Tarea editada:', data);

    })
    .catch(error => console.error('Error:', error));
}


//Delete task.
var deleteTask=function(){
	console.log("Delete Task...");
	var listItem=this.parentNode;
    var taskId = listItem.getAttribute('data-id');
	fetch(`/moneitas/api/delete_task/${taskId}/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      }
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        console.log('Tarea eliminada con éxito.');
      })
      .then(data => {
        console.log('Tarea eliminada con éxito:', data);
        var listItem=this.parentNode;
	    var ul=listItem.parentNode;
		//Remove the parent list item from the ul.
		ul.removeChild(listItem);
      })
      .catch(error => {
        console.error('Error al eliminar la tarea:', error);
        console.error('Mensaje de error:', error.message);
      });
}


//Mark task completed
var taskCompleted=function(){
	console.log("Complete Task...");
    var listItem=this.parentNode;
    taskState('complete', listItem);

	//Append the task list item to the #completed-tasks
	completedTasksHolder.appendChild(listItem);
	bindTaskEvents(listItem, taskIncomplete);

}

//Mark task as incomplete.
//When the checkbox is unchecked
var taskIncomplete=function(){
	console.log("Incomplete Task...");
    var listItem=this.parentNode;
    taskState('incomplete', listItem);
	//Append the task list item to the #incomplete-tasks.
	incompleteTaskHolder.appendChild(listItem);
	bindTaskEvents(listItem,taskCompleted);
}

var taskState=function(new_state, listItem){
    var taskId = listItem.getAttribute('data-id');
    var taskData = {
        state: new_state,
    };
    editTask(taskData, taskId);

}



//The glue to hold it all together.


//Set the click handler to the addTask function.
addButton.onclick=addTask;
//addButton.addEventListener("click",addTask);


var bindTaskEvents=function(taskListItem,checkBoxEventHandler){
	console.log("bind list item events");
//select ListItems children
	var checkBox=taskListItem.querySelector("input[type=checkbox]");
	var editButton=taskListItem.querySelector("button.edit");
	var deleteButton=taskListItem.querySelector("button.delete");


			//Bind editTask to edit button.
			editButton.onclick=editTaskname;
			//Bind deleteTask to delete button.
			deleteButton.onclick=deleteTask;
			//Bind taskCompleted to checkBoxEventHandler.
			checkBox.onchange=checkBoxEventHandler;
}

//cycle over incompleteTaskHolder ul list items
	//for each list item
	for (var i=0; i<incompleteTaskHolder.children.length;i++){

		//bind events to list items chldren(tasksCompleted)
		bindTaskEvents(incompleteTaskHolder.children[i],taskCompleted);
	}




//cycle over completedTasksHolder ul list items
	for (var i=0; i<completedTasksHolder.children.length;i++){
	//bind events to list items chldren(tasksIncompleted)
		bindTaskEvents(completedTasksHolder.children[i],taskIncomplete);
	}
