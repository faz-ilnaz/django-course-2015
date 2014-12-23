"use strict";
App.controller("ProjectCtrl", function ($scope, $http, $cookies) {

    $scope.init = function () {
        $http.get('/api/projects').success(function(response){
            $scope.projectsModel = response;
        });
    };

    $scope.getAllProjects = function(){
       $http.get('/api/projects').success(function(response){
            $scope.projectsModel = response;
       });
    };

    $scope.addProject = function(){
        var inData= {name: $scope.newProject};
        $http.post('/api/projects/',  inData).success(function(response){
            $scope.projectsModel.push(response);
        });
        $scope.newProject = '';
    };

	$scope.deleteProject = function  (project) {
        $http.delete('/api/projects/' +  project.id).success(function(response){
            var index = $scope.projectsModel.indexOf(project);
            $scope.projectsModel.splice(index, 1);
        });

    };

    $scope.updateProject = function(project) {
        return $http.put('/api/projects/' +  project.id, project)
     };




	$scope.$watch("projects",function  (newVal,oldVal) {
		if (newVal !== null && angular.isDefined(newVal) && newVal!==oldVal) {
            $http.post('/api/projects/',  angular.toJson(newVal)).success(function(response){

            });
		}
	},true);
});