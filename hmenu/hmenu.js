//All of the lines that have been piped into the program
var lines = [];
//The chosen element
var chosen = '';

//Called by python to add a line to the list of lines
function add_lines(l){
    //lines.push(line);
    lines = l;
    populateLines();
}

//Creates a div for each line
function populateLines(){
    var query = $('#input').val().toLowerCase();
    var total = 0;
    var i = 0;
    var divs = "";
    var matchingLines = [];
    var line;

    //find all matching lines
    while( total<128 && i<lines.length){
        line = lines[i];
        if( line.toLowerCase().indexOf(query) != -1 ){
            matchingLines.push(line);
            total++;
        }
        i++;
    }

    //sort the matching elements by length
    matchingLines.sort(function(a, b){
        if( a.length==b.length ){
            return a.localeCompare(b);
        }else{
            return a.length - b.length;
        }
    });
    chosen = query;
    for( i=0; i<matchingLines.length; i++ ){
        line = matchingLines[i];
        if( i == 0 ){
            divs += '<div class="line chosen">'+line+'</div>';
            chosen = line;
        }else{
            divs += '<div class="line">'+line+'</div>';
        }
    }

    $('.container')
        .empty()
        .append(divs);
}

function init(){
    //Set up the input div
    $('body')
    .append('<div class="launcher"><form id="form" action="javascript:void(0);"><input id="input" type="text" /></form></div>')
    .append('<div class="container"></div>')

    //Never lose focus
    $("#input").focus();
    $("#input").blur(function(){$("#input").focus()});
    $("#input").keyup(populateLines);
    $("#form").submit(function(){py_post(chosen);});

    //play intro animation
//    $('.launcher').tween({
//        top:{
//            start: -40,
//            stop: 20,
//            time: 0,
//            duration: .25,
//            units: 'px',
//            effect: 'easeInOut',
//            onStop: function(){
//                $('.container').tween({
//                    opacity:{
//                        start: 0,
//                        stop: 100,
//                        time: 0,
//                        duration: .15,
//                        units: '%',
//                        effect: 'easeInOut'
//                    }
//                });
//            }
//        }
//    });
    $('body').tween({
        opacity:{
            start: 0,
            stop: 100,
            time: 0,
            duration: .25,
            units: '%',
            effect: 'easeInOut'
        }
    });
    $.play();
}

//kick everything off once the page is loaded
$('body').ready(init);

