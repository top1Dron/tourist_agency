$(document).ready(function () {
    // function to get cookie - need to send crsftoken
    function getCookie(name) {

        var matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
        ))
        return matches ? decodeURIComponent(matches[1]) : undefined
    };

    // $('select[multiple]').multiSelect();

    $(document).on('click', '#find-tours-button', function(e) {
        e.preventDefault();

        var url = $("#findAvailableToursForm").attr("find-tours-url");
        var countryName = $("#id_tour_country_name").val();
        var citiesId = $("#id_tour_city_name").val();
        var hotelName = $("#id_tour_hotel_name").val();
        var departureDate = $("#id_departure_date").val();
        var nightCount = $("#id_night").val();
        var departureCityName = $("#id_tour_departure_city_name").val();

        $.ajax({
            url: url,
            type: "POST",
            dataType: 'json',
            data: {
              csrfmiddlewaretoken: getCookie('csrftoken'),
              'country': countryName,
              'city[]': citiesId,
              'hotel[]': hotelName,
              'departure_date':departureDate,
              'night_count':nightCount,
              'departure_city':departureCityName
            },
            beforeSend: function () {
              $("#available-tours-task-modal").modal("show");
            },
            success: function (data) {
              $("#available-tours-task-modal .modal-content").html(data.html_available_tours);
            // $("#available_tours_form").html(data);
        }
        });
        return false;
    });

    $("#id_tour_hotel_name").multiSelect('refresh');
    $("#id_tour_city_name").multiSelect('refresh');
    $('#id_tour_country_name').niceSelect();
    $('#id_tour_departure_city_name').niceSelect();
    $("#id_departure_date").datepicker({dateFormat:"dd.mm.yy", 
    monthNames: [ "Січень", "Лютий", "Березень", "Квітень", "Травень", "Червень", "Липень", "Серпень", "Вересень", "Жовтень", "Листопад", "Грудень" ],
    dayNamesMin: [ "Нед", "Пон", "Вів", "Сер", "Чет", "П'ят", "Суб"],
    minDate: "+2d", maxDate: "+2d +1m",
  });

    function check_hotels_on_change_country(){
        var url = $("#findAvailableToursForm").attr("data-country-hotels");
        var countryId = $("#id_tour_country_name").val();
  
        $.ajax({
          url: url,
          data: {
            'country': countryId
          },
          success: function (data) {
            // console.log(document.getElementById("ms-id_tour_city_name").innerHTML);
            $("#id_tour_hotel_name").html(data);
            $('#id_tour_hotel_name').multiSelect('refresh');
          }
        });
    }

    $("#id_tour_country_name").change(function () {
        
        var url = $("#findAvailableToursForm").attr("data-cities-url");
        // const selected = document.querySelectorAll('#id_tour_country_name option:checked');
        // const countryId = Array.from(selected).map(el => el.value);
        var countryId = $(this).val();
  
        $.ajax({
          url: url,
          data: {
            'country': countryId
          },
          success: function (data) {
            
            $("#id_tour_city_name").html(data);
            $('#id_tour_city_name').multiSelect('refresh');
          }
        });
        check_hotels_on_change_country();
    });

    $("#id_tour_city_name").change(function (e) {
        e.preventDefault();
        var url = $("#findAvailableToursForm").attr("data-hotels-url");
        var citiesId = Array.from(document.getElementById('id_tour_city_name').selectedOptions).map(el=>el.value);
        // var citiesId = $("#id_tour_city_name").val();
        if(citiesId != null){
          citiesId = citiesId.join(',')
        }
  
        $.ajax({
          url: url,
          data: {
            'city': citiesId
          },
          success: function (data) {
            // console.log(document.getElementById("ms-id_tour_city_name").innerHTML);
            $("#id_tour_hotel_name").html(data);
            $('#id_tour_hotel_name').multiSelect('refresh');
          }
        });
        return false;
    });
})