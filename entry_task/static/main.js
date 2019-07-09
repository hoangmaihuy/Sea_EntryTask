const domain = window.location.origin;

function handleLogin() {
    let username = $('#username').val();
    let password = $('#password').val();
    let data = {
        "username": username,
        "password": password
    };
    $.post('/api/login', JSON.stringify({"username": username}),
        function(data) {
            console.log(data);
            if (!data.error) {
                let key = data.content.key;
                let hash_password = CryptoJS.SHA256(password).toString();
                console.log(hash_password);
                let encrypted_password = CryptoJS.AES.encrypt(hash_password, key, {}).toString();
                console.log(encrypted_password);
                $.post('/api/login', JSON.stringify({"username": username, "password": encrypted_password}),
                    function(data) {
                        console.log(data);
                        $('#status').text(data.status);
                        if (!data.error) {
                            let token = data.content.token;
                            localStorage.setItem('token', token);
                            $(location).attr('href', '/events/1');
                        }
                    }
                );
            }
        }
    );
}


function getEventDetail(event_id) {
    let request = {
        "event_id": event_id
    };
    let token = localStorage.getItem('token');
    $.ajax({
        url: '/api/event',
        type: 'post',
        headers: {'token' : token},
        dataType: 'json',
        contentType: 'application/json',
        traditional: false,
        data: JSON.stringify({"event_id": event_id}),
        success: function(response) {
            console.log(response);
            if (!response.error) {
                let content = response.content;
                $("#title").text(content.title);
                $("#description").text(content.description);
                $("#date").text(content.date);
                $("#location").text(content.location);
                $("#photo").attr("src", content.photo_url);

                let categories = content.categories.split(',');
                for (let category of categories) {
                    let url = '#'
                    let html_content = '<li style="display: inline"><a href='+ url +'>#' + category + ' </a></li>';
                    $('#categories').append(html_content);
                }
            } else alert(response.status);
        }
    });

    $.ajax({
        url: '/api/event/get_likes',
        type: 'post',
        headers: {'token' : token},
        dataType: 'json',
        contentType: 'application/json',
        traditional: false,
        data: JSON.stringify({"event_id": event_id, "offset": 0, "size": 10})
    }).done(function(response) {
        let likes = response.content;
        $("#likesCount").text(likes.length);
        for (let user of likes) {
            $("#likes").append(
              '<li style="display: inline">' + user + ' </li>'
            );
        }
    });

    $.ajax({
        url: '/api/event/get_participants',
        type: 'post',
        headers: {'token' : token},
        dataType: 'json',
        contentType: 'application/json',
        traditional: false,
        data: JSON.stringify({"event_id": event_id, "offset": 0, "size": 10})
    }).done(function(response) {
        let participants = response.content;
        $("#participantsCount").text(participants.length);
        for (let user of participants) {
            $("#participants").append(
              '<li style="display: inline">' + user + ' </li>'
            );
        }
    });

    $.ajax({
        url: '/api/event/get_comments',
        type: 'post',
        headers: {'token' : token},
        dataType: 'json',
        contentType: 'application/json',
        traditional: false,
        data: JSON.stringify({"event_id": event_id, "offset": 0, "size": 10}),
        success: function(response) {
            console.log(response);
            if (!response.error) {
                let comments = response.content;
                for (let i in comments) {
                    let html_content = '<li>' + comments[i].by_user + ': ' + comments[i].content  + '</li>'
                    $('#comments').append(html_content);
                }
            } else alert(response.status);
        }
    });
}

function renderEvents(eventList) {
    let token = localStorage.getItem('token');
    for (let event_id of eventList) {
        let categoriesList = "";
        $.ajax({
            url: '/api/event',
            type: 'post',
            headers: {'token' : token},
            dataType: 'json',
            contentType: 'application/json',
            traditional: false,
            data: JSON.stringify({"event_id" : event_id})
        }).done(function(response) {
            let event = response.content;
            let event_url = domain + "/event/" + event_id;
            let categories = event.categories.split(',');
            for (let category of categories) {
                let url = '#';
                let html_content = '<li style="display: inline"><a href='+ url +'>#' + category + ' </a></li>';
                categoriesList += html_content;
            }
            let html_content = '<tr>' +
            '<td>' + event.id + '</td>' +
            '<td><a href=' + event_url +'>' + event.title + '</a></td>' +
            '<td>' + event.location + '</td>' +
            '<td>' + event.date + '</td>' +
            '<td>' + categoriesList + '</td>' +
            '</tr>';
            $('#event_table').after(html_content);
        });
    }
}

function getEventsPage(page_id) {
    let url = window.location.origin + "/events/";
    $('a[href="/Previous"]').attr('href', url + (page_id-1));
    $('a[href="/Next"]').attr('href', url + (page_id+1));
    let token = localStorage.getItem('token');
    let size = 10;
    let offset = (page_id-1)*size;
    let start_date = localStorage.getItem("start_date");
    let end_date = localStorage.getItem("end_date");
    let category = localStorage.getItem("category");
    let request = {
        "offset": offset,
        "size": size
    };
    if (start_date) request["start_date"] = start_date;
    if (end_date) request["end_date"] = end_date;
    if (category) request["category"] = category;
    console.log(request);
    $.ajax({
        url: '/api/events',
        type: 'post',
        headers: {'token' : token},
        dataType: 'json',
        contentType: 'application/json',
        traditional: false,
        data: JSON.stringify(request)
    }).done(function(response) {
        console.log(response);
        if (!response.error) {
            let events = response.content;
            console.log(events);
            renderEvents(events);
        } else alert(response.status);
    });
}

function submitComment(event_id) {
    let token = localStorage.getItem('token');
    let content = $("#new_comment").val();
    let request = {
        "event_id": event_id,
        "content": content
    };
    $.ajax({
        url: '/api/event/add_comment',
        type: 'post',
        headers: {'token' : token},
        dataType: 'json',
        contentType: 'application/json',
        traditional: false,
        data: JSON.stringify(request),
        success: function(response) {
            console.log(response);
            if (!response.error) {
                document.location.reload();
            } else alert(response.status);
        }
    });
}

function likeEvent(event_id) {
    let token = localStorage.getItem('token');
    $.ajax({
        url: '/api/event/add_like',
        type: 'post',
        headers: {'token' : token},
        dataType: 'json',
        contentType: 'application/json',
        traditional: false,
        data: JSON.stringify({"event_id" : event_id}),
        success: function(response) {
            console.log(response);
            if (!response.error) {
                document.location.reload();
            } else alert(response.status);
        }
    });
}

function participateEvent(event_id) {
    let token = localStorage.getItem('token');
    $.ajax({
        url: '/api/event/add_participant',
        type: 'post',
        headers: {'token' : token},
        dataType: 'json',
        contentType: 'application/json',
        traditional: false,
        data: JSON.stringify({"event_id" : event_id}),
        success: function(response) {
            console.log(response);
            if (!response.error) {
                document.location.reload();
            } else alert(response.status);
        }
    });
}

function submitEvent() {
    let token = localStorage.getItem('token');
    let title = $('#title').val();
    let location = $('#location').val();
    let date = $('#date').val();
    console.log(date);
    let description = $('#description').val();
    let categories = $('#categories').val();
    let photo = document.querySelector('input[type=file]').files[0];
    let photo_url = '';
    if (photo) {
        console.log("uploading");
        let formData = new FormData();
        formData.append("image", photo);
        $.ajax({
            url: domain+'/admin/upload_photo',
            type: 'post',
            headers: {'token' : token},
            data: formData,
            processData: false,
            contentType: false,
            async: false,
        }).done(function(response) {
            photo_url = response.content.photo_url;
            console.log(response);
        });
    }
    let request = {
        "title": title,
        "location": location,
        "date": date+'Z',
        "description": description,
        "categories": categories.split(','),
        "photo_url" : photo_url
    };
    console.log(date);
    $.ajax({
        url: '/admin/create_event',
        type: 'post',
        headers: {'token' : token},
        dataType: 'json',
        contentType: 'application/json',
        traditional: false,
        data: JSON.stringify(request),
        success: function(response) {
            if (!response.error) {
                let event = response.content;
                $(window.location).attr('href', domain + '/event/' + event.id);
            } else alert(response.status);
        }
    });
}

function toCreateEvent() {
    $(location).attr('href', domain + '/event/create');
}

function filterEvents() {
    let start_date = $("#start_date").val();
    let end_date = $("#end_date").val();
    let category = $("#category").val();
    if (start_date && end_date) {
        console.log(start_date, end_date);
        localStorage.setItem("start_date", start_date+":00Z");
        localStorage.setItem("end_date", end_date+":00Z");
        localStorage.removeItem("category");
    }
    if (category) {
        localStorage.setItem("category", category);
        localStorage.removeItem("start_date");
        localStorage.removeItem("end_date");
    }
    $(location).attr('href', domain + '/events/1');
}