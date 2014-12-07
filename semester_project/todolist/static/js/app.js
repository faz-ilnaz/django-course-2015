/*!
** Todo-Sortable-List Example App
** Licensed under the Apache License v2.0
** http://www.apache.org/licenses/LICENSE-2.0
** Built by Jay Kanakiya ( @techiejayk )
**/
"use strict";

var App = angular.module("todo", ["ui.sortable", 'ngCookies']);

App.controller("TodoCtrl", function ($scope, $http, $cookies) {

    $scope.init = function () {
        $http.get('/api/projects').success(function(response){
            $scope.model = response;
        });
        $scope.show = "All";
        if($cookies.currentShow) {
            $scope.currentShow = parseInt($cookies.currentShow);
        } else {
            $scope.currentShow = 0;
        }
    };

    $scope.getAllTodos = function(){
       $http.get('/api/projects').success(function(response){
            $scope.model = response;
       });
       $scope.show = "All";
    };

//	$scope.addTodo = function  () {
//		/*Should prepend to array*/
//		$scope.model[$scope.currentShow].tasks.splice(0, 0, {title: $scope.newTodo, isDone: false });
//		/*Reset the Field*/
//		$scope.newTodo = "";
//	};

    $scope.addTodo = function(){
        var inData= {title: $scope.newTodo, isDone: false, project: $scope.model[$scope.currentShow].id};
        $http.post('/api/tasks/',  inData).success(function(response){
//            $scope.getAllTodos();
            $scope.model[$scope.currentShow].tasks.push(response);
        });
        $scope.newTodo = '';
    };

	$scope.deleteTodo = function  (task) {
        $http.delete('/api/tasks/' +  task.id).success(function(response){
//            $scope.getAllTodos();
            var index = $scope.model[$scope.currentShow].tasks.indexOf(task);
            $scope.model[$scope.currentShow].tasks.splice(index, 1);
        });

    };

	$scope.todoSortable = {
		containment: "parent",//Dont let the user drag outside the parent
		cursor: "move",//Change the cursor icon on drag
		tolerance: "pointer"//Read http://api.jqueryui.com/sortable/#option-tolerance
	};

	$scope.changeTodo = function  (i) {
		$scope.currentShow = i;
        $cookies.currentShow = i;
	};

	/* Filter Function for All | Incomplete | Complete */
	$scope.showFn = function  (todo) {
		if ($scope.show === "All") {
			return true;
		}else if(todo.isDone && $scope.show === "Complete"){
			return true;
		}else if(!todo.isDone && $scope.show === "Incomplete"){
			return true;
		}else{
			return false;
		}
	};

    $scope.toggleTodoItemStatus = function(task) {
       task.isDone = !task.isDone;

        $http.put('/api/tasks/' +  task.id, task).success(function(response){
//            $scope.getAllTodos();

        });
    };

//	$scope.$watch("model",function  (newVal,oldVal) {
//		if (newVal !== null && angular.isDefined(newVal) && newVal!==oldVal) {
//			localStorageService.add("todoList",angular.toJson(newVal));
//		}
//	},true);

});




App.run(function($rootScope, $http, $cookies){
    // set the CSRF token here
    $http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken;
});



