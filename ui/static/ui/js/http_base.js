function getProjects(){
    $.getJSON( "/apis/projects", function(data){
        $.each(data, function(){
            var object = this;
            var items = [];
            items.push( "<li> id: " +object["id"] + "</li>" );
            items.push( "<li> <a href=\"/projects/"+object["id"]+"\">name: "+object["name"]+"</a></li>" );
            items.push( "<li> create_date: " +object["create_time"] + "</li>" );
            $( "<ul/>", {
                "class": "project-detail-list",
                html: items.join( "" )
            }).appendTo( "#projectList");
        });
    });
}

function getProjectModules(projectId){
    $.getJSON( "/apis/projects/"+projectId+"/modules", function (data){
        $.each(data, function(){
            var object = this;
            var items = [];
            var module_id = object["id"];
            items.push( "<li> id: " +module_id + "</li>" );
            var click_func = '"getModuleCases('+module_id+');"';
            items.push( "<li onclick="+click_func+" > name: "+object["name"]+"</li>" );
            $( "<ul/>", {
                "class": "modules-detail-list",
                "id": "module"+object["id"],
                html: items.join( "" )
            }).appendTo( "#moduleList" );
        });
    });
}

function getModuleCases(moduleId){
    $.getJSON( "/apis/modules/"+moduleId+"/cases", function (data){
        $.each(data, function(){
            var object = this;
            var items = [];
            items.push( "<li> id: " +object["id"] + "</li>" );
            items.push( "<li> <a href=\"/cases/"+object["id"]+"/requests\">name: "+object["name"]+"</a></li>" );
            $( "<ul/>", {
                "class": "modules-detail-list",
                html: items.join( "" )
            }).appendTo( "#module"+moduleId );
        });
    });
}



