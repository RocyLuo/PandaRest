function get_projects(){
    $.getJSON( "apis/projects", get_projects_callback);
}

function get_projects_callback(data){
    $.each(data, function(){
        var object = this;
        var items = [];
        items.push( "<li> id: " +object["id"] + "</li>" );
        items.push( "<li> <a href=\"/projects/"+object["id"]+"\">name: "+object["name"]+"</a></li>" );
        items.push( "<li> create_date: " +object["create_time"] + "</li>" );
        $( "<ul/>", {
            "class": "my-new-list",
            html: items.join( "" )
        }).appendTo( "body" );
    });
}

get_projects();
