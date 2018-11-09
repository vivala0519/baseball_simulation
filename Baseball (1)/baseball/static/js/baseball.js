
$(document).ready(function() {
    //branch test
    // 선수 검색
    $('.search').click(function (){

        $.ajax({
            url:'/game/SearchPlayer/',              //game : 앱이름
            type:'POST',
            dataType: "json",
            contentType : 'application/x-www-form-urlencoded; charset=utf-8',
            data : {'searchStr' : $('.searchStr').val()},

            success:function(data) {
                $('#output').empty();
                $.each(data, function(index, item){
                      alert("데이터들어옴");
                   var output = '';
                   output += item.year + ', ';
                   output += item.team + ', ';
                   output += item.position + ', ';
                   output += item.player + ', ';
                   output += '&nbsp' + '<button type="button" class="btn btn-dark" id="playerCheck">선택</button>'
                   console.log("output:" + output);
                   $('#output').append(output);
                });
            },
            error:function(){
                alert("ajax통신 실패!!!");
            }
        });
    });
    /*on 태그가 동적?생성시 사용*/
    /*$('#playerCheck').on(function (){*/
    $(document).on("click","#playerCheck",function(){
        alert("선수선택");
    });




     $( ".sortable" ).sortable({
      revert: true
    });
    $( "#draggable" ).draggable({
      connectToSortable: "#.sortable",
      helper: "clone",
      revert: "invalid"
    });
    $( "ul, li" ).disableSelection();


    $( "#Result" ).on( "click", function() {
     $( "#effect" ).show( 'Blind');
    });

    /*$('#Rhide').on( "click", function() {
     $( "#effect" ).hide( 'Blind');
    });*/

    //추가하기 버튼 눌렀을 때
    $('#search2').on('click', function(){
        var players;
        var isData;
        //var playerList=[][];
        var detail=[];

        var selectMyTeam = $('#myTeam option:selected').text();
        var selectYear = $('#year option:selected').text();
        var selectTeam = $('#team option:selected').text();
        var selectHp = $('#hp option:selected').text();
        var selectPosition = $('#position option:selected').text();
        var selectPlayer = $('#player option:selected').text();
        var teamIdx = $('#myTeam option:selected').attr('name');
        alert(selectTeam)

        if(selectMyTeam == '팀정하기' || selectPlayer == '선수명'){
            alert('조건을 모두 선택해주세요');
        }else{
            if(playerList.length == 12){
                return null;
            }

            //isData = $.inArray(selectPlayer, playerList);       //이 리스트에 selectPlayer가 몇번째 위치에 있는지 인덱스값반환, 리스트에 없으면 -1
            //if(isData < 0 ){
            for(var i=1; i<=12; i++){
                 players = $('#team'+teamIdx+' li:nth-child('+i+')').text();
                if(players ==  'Player'){
                    detail.push(selectPlayer)       //,selectYear,selectTeam,selectHp,selectPosition
                    alert('detail 1: ', detail)
                    detail.push(selectYear)
                     alert('detail 2: ', detail)
                    //playerList.push(detail)
                    $('#team'+teamIdx+' li:nth-child('+i+')').text(selectPlayer);
                    break;
                }
            }
        }
    });

    // 선수 목록에서 삭제할 때
    $('.delete button').on('click', function(){
        var isData;
        var idx = $(this).val();
        var teamIdx = $(this).attr('name');
        var players = $("#team"+ teamIdx +" li:nth-child("+idx+")").text();

        $("#team"+ teamIdx +" li:nth-child("+idx+")").text('Player');
    });

    //record-tab
    $( function() {
        $( "#tabs" ).tabs();
    });

    //Game Start 버튼 눌렀을 때
    $('#start').on('click', function(){
        var i;
        var players;
        var check;
        var teamIdx;

    Outer:
        for(teamIdx=1; teamIdx<=2; teamIdx++){
            for(i=1; i<=2; i++){                        // 2 ->12로 바꿔라
                players = $('#team'+ teamIdx +' li:nth-child('+i+')').text();
                if(players == 'Player'){
                    alert('12명의 선수를 모두 선택해주세용');
                    break Outer;
                }
                if($('#t'+teamIdx+'Name').val() == ''){
                    alert('팀의 이름을 정해주세요');
                    break Outer;
                }
            }
            if(teamIdx == 2)
                check = 1;
        }

        var score_1 = [10,10,10,0,2,2,1,1,0,49,8,4,5]
        var score_2 = [1,2,7,0,5,0,4,1,'-',20,11,0,4]
        if (check == 1){
            $('#result').attr('disabled', true);    // 게임시작하면 끝날 때까지 기록보기버튼 비활성화시키기

            $('#record_tab div p').empty();         //경기 내용 삭제
            $("#effect" ).hide( 'Blind');           //주요 기록 숨기기
            $('#score_board tbody td').empty();
            $('#score_board tbody th').empty();

            /*
            for(teamIdx=1; teamIdx<=2; teamIdx++){
                $('#score_board tbody tr:nth-child(' +teamIdx+ ') > th').text($('#t'+teamIdx+'Name').val())
                if(teamIdx == 1){
                    score = score_1
                }else{
                    score = score_2
                }
                for(i=0;i<=12;i++){
                    if(i==9){
                        $('#score_board tbody tr:nth-child(' +teamIdx+ ') >td:nth-child('+(i+2) + ')').html('<strong>'+score[i]+'</strong>')
                        continue;
                    }
                    $('#score_board tbody tr:nth-child(' +teamIdx+ ') >td:nth-child('+(i+2) + ')').text(score[i])
                    // td 값은 td:nth-child(2)부터 시작해서 14까지대입      @@왠지는 몰라
                }
            }*/
        }
    socketStart();
    $('#result').attr('disabled', false);
    });


    // 주요기록보기 버튼눌렀을 때
    $('#Result').on('click', function(){
        var teamIdx;
        var teamName =[];
        alert('anjdi')
        for(teamIdx=1; teamIdx<=2; teamIdx++){
            teamName.push($('#score_board tbody tr:nth-child(' +teamIdx+ ') > th').text())
        }
        html = ''
        html += '<h4>'+teamName[0]+'</h4>'
        html += '<p>'+$('#score_board tbody tr:nth-child(1) >td:nth-child(2)').text() +'</p>'
        html += '<h4>'+teamName[1]+'</h4>'
        html += '<p>'+$('#score_board tbody tr:nth-child(2) >td:nth-child(2)').text() +'</p>'
        alert(html)
        $('#record_tab #tabs-1 p').html(html);

    });


});   //$ready문 끝



