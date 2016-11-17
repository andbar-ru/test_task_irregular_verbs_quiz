function get_qvf() { //{{{1
  var qvf = $('input[name="qvf"]:checked').val();
  if (!(qvf in {'1':'', '2':'', '3':''})) {
    qvf = '1';
  }
  return qvf;
}

//}}}
function get_avf() { //{{{1
  var avf = $('input[name="avf"]:checked').val();
  if (!(avf in {'1':'', '2':'', '3':''})) {
    avf = '2';
  }
  return avf;
}

//}}}
function get_stats() { //{{{1
  $.get('/stats/', function(result) {
    var parts = result.trim().split(',');
    var yesPart = parts[0];
    var noPart = parts[1];
    var yes = parseInt(yesPart.split(':')[1]);
    var no = parseInt(noPart.split(':')[1]);
    $('#yes').html(yes);
    $('#no').html(no);
  });
}

//}}}
$(document).ready(function() { //{{{1

  get_stats();

  $('#requestVerb').click(function() {
    var qvf = get_qvf();
    $.get('/quiz/?'+qvf)
      .done(function(result) {
        $('#question').val(result.trim());
      })
      .fail(function(jqxhr) {
        $('#errors').html(jqxhr.responseText.trim());
      });
    return false;
  });

  $('#submitAnswer').click(function() {
    $('#errors').empty();
    $('#result').empty();
    var qvf = get_qvf();
    var avf = get_avf();
    if (qvf == avf) {
      $('#errors').html('ERROR: verb forms must be different!');
      return false;
    }
    var question = $('#question').val().trim();
    if (question == '') {
      $('#errors').html('ERROR: question is empty!');
      return false;
    }
    var answer = $('#answer').val().trim();
    if (answer == '') {
      $('#errors').html('ERROR: answer is empty!');
      return false;
    }
    var postData = {};
    postData[answer] = '';
    var url = '/quiz/'+question+'/?'+qvf+','+avf;
    $.post(url, postData)
      .done(function(result) {
        $('#result').html(result);
        $('#answer').val('');
        $('#requestVerb').click();
        get_stats();
      })
      .fail(function(jqxhr) {
        $('#errors').html(jqxhr.responseText.trim());
      });
    return false;
  });
  
});

//}}}
