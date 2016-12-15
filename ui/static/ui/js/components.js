// Register `phoneList` component, along with its associated controller and template
angular.
  module('myApp').
  component('phoneList', {
    template:
        '<ul>' +
          '<li ng-repeat="phone in $ctrl.phones">' +
            '<span>{{phone.name}}</span>' +
            '<p>{{phone.snippet}}</p>' +
          '</li>' +
        '</ul>',
    controller: function PhoneListController() {
      this.phones = [
        {
          name: 'Nexus S',
          snippet: 'Fast just got faster with Nexus S.'
        }, {
          name: 'Motorola XOOM™ with Wi-Fi',
          snippet: 'The Next, Next Generation tablet.'
        }, {
          name: 'MOTOROLA XOOM™',
          snippet: 'The Next, Next Generation tablet.'
        }
      ];
    }
  });


angular.
  module('myApp').
  component('projectList', {
    template:
        '<ul>' +
          '<li ng-repeat="project in projects">' +
            '<span>{{project.id}}</span>' +
            "<a href=\"/projects/{{project.id}}\">name: {{project.name}}</a>" +
          '</li>' +
        '</ul>',
    controller: function ProjectListController($scope, $http) {
      $http.get("/apis/projects"
          ).then(function successCallback(data) {
            $scope.projects = data['data']
          }, function errorCallback(response) {
            // called asynchronously if an error occurs
            // or server returns response with an error status.
          });
    }
  });

angular.
  module('myApp').
  component('navTree',{
    template:
        '<ul>' +
          '<li ng-repeat="module in modules">' +
            '<span>{{module.id}}</span>' +
            "<a href=\"/projects/{{project.id}}\">name: {{module.name}}</a>" +
          '</li>' +
        '</ul>',
    controller: function Controller($scope, $http) {
      $http.get("/apis/projects"+$scope.project_id+"/modules"
          ).then(function successCallback(data) {
            $scope.modules = data['data']
          }, function errorCallback(response) {
            // called asynchronously if an error occurs
            // or server returns response with an error status.
          });
    }
  });