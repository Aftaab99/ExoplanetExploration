const planetsPresentForm = `
<form class="mt-2 form-inline" name='planetsPresentForm'>
    <select class="form-control">
        <option value="Gliese 876 b">Gliese 876 b</option>
        <option value="Gliese 876 c">Gliese 876 c</option>
        <option value="Gliese 876 e">Gliese 876 e</option>
        <option value="Mercury">Mercury</option>
        <option value="Venus">Venus</option>
        <option value="Earth">Earth</option>
        <option value="Mars">Mars</option>
        <option value="Jupiter">Jupiter</option>
        <option value="Saturn">Saturn</option>
        <option value="Uranus">Uranus</option>
        <option value="Neptune">Neptune</option>
        <option value="Pluto">Pluto</option>
        <option value="KOI-142 b">KOI-142 b</option>
        <option value="KOI-142 c">KOI-142 c</option>
    </select>
    <button class="btn btn-success ml-2" type="submit" name="dataset-planet-orbit-dist">Find location</button>
</form>
`;

const otherPlanetsForm = `
<form class="mt-2" name="otherPlanetsForm">
    <div class="container mt-2">
        <div class="row mb-2">
            <input type="text" class="form-control col-md-5 col-sm-12" name="semi-major-axis" required="required"
                        placeholder="Semi major axis (AU)" data-error="Please enter a valid number">
            <input type="text" class="form-control col-md-5 col-sm-12 ml-md-5 mt-sm-2 mt-md-0" name="eccentricity" required="required"
                        placeholder="Eccentricity" data-error="Please enter a valid number">
        </div>
        <div class="row mb-2">
            <input type="text" class="form-control col-md-5 col-sm-12" name="ascending-node" required="required"
                        placeholder="Ascending node longitude(degree)" data-error="Please enter a valid number">
            <input type="text" class="form-control col-md-5 col-sm-12 ml-md-5 mt-sm-2 mt-md-0" name="periastron" required="required"
                        placeholder="Periastron(degree)" data-error="Please enter a valid number">
        </div>
        <div class="row mb-2">
            <input type="text" class="form-control col-md-5 col-sm-12" name="period" required="required"
                        placeholder="Orbital period(days)" data-error="Please enter a valid number">
            <input type="text" class="form-control col-md-5 col-sm-12 ml-md-5 mt-sm-2 mt-md-0" name="dates" required="required"
                        placeholder="Measurement date(DD/MM/YYYY)" data-error="Please enter a valid number">
        </div>
        <div class="row mb-3">
            <input type="text" class="form-control col-md-5 col-sm-12" name="mean-longitude-degrees" required="required"
                        placeholder="Mean longitude(degrees)" data-error="Please enter a valid number">
            <input type="text" class="form-control col-md-5 col-sm-12 ml-md-5 mt-sm-2 mt-md-0" name="inclination" required="required"
                        placeholder="Inclination(degrees)" data-error="Please enter a valid number">
        </div>
        <center>
            <button class="btn btn-success" type="submit" name="otherPlanetsSubmit">Find position</button>
        </center>
    </div>
</form>
`;
$('#selected-form-type').html(planetsPresentForm);
$("form[name='planetsPresentForm']").on('submit', function (event) {
    event.preventDefault();
    let planetName = $(this).find('select').val();
    $.ajax({
        data: {
            PlanetName: planetName
        },
        type: 'POST',
        url: '/orbit_position_present'

    }).done(function (data) {
        if (data.error == 0) {
            let radius_vector = data.radius_vector;
            let ra = data.RA;
            let dec = data.DEC;
            let res = `<p class="mt-2">The planet is at a distance of ${radius_vector} AU from its host star. Spherical coordinates are right ascention=${ra}, declination=${dec}. These are the positions in orbit with respect to the host star right now and will differ from the average values as not all orbits are circular.</p>`
            $('#orbit-position-result').html(res);
        } else {
            let res = `<h6 class="mt-2">Oops, something went wrong</h6>`
            $('#result-calc-distance').html(res);
        }
    });

});
var form_type;
$('input[name="planet-choice"]').change(function () {
    form_type = $('input[name="planet-choice"]:checked').val();
    if (form_type == "0") {
        $('#selected-form-type').html(planetsPresentForm);

        $("form[name='planetsPresentForm']").on('submit', function (event) {
            event.preventDefault();
            let planetName = $(this).find('select').val();
            $.ajax({
                data: {
                    PlanetName: planetName
                },
                type: 'POST',
                url: '/orbit_position_present'

            }).done(function (data) {
                if (data.error == 0) {
                    let radius_vector = data.radius_vector;
                    let ra = data.RA;
                    let dec = data.DEC;
                    let res = `<p class="mt-2">The planet is at a distance of ${radius_vector} AU from its host star. Spherical coordinates are right ascention=${ra}, declination=${dec}. These are the positions in orbit with respect to the host star right now and will differ from the average values as not all orbits are circular.</p>`
                    $('#orbit-position-result').html(res);
                } else {
                    let res = `<h6 class="mt-2">Oops, something went wrong</h6>`
                    $('#result-calc-distance').html(res);
                }
            });

        });
    } else {
        $('#selected-form-type').html(otherPlanetsForm);
        $("form[name='otherPlanetsForm']").on('submit', function (event) {
            event.preventDefault();
            var inputs_valid = false;

            var a = $("input[name='semi-major-axis']").val();
            var ecc = $('input[name="eccentricity"]').val();
            var asc_long = $('input[name="ascending-node"]').val();
            var inc = $('input[name="inclination"]').val();
            var arg_per = $('input[name="periastron"]').val();
            var dates = $('input[name="dates"]').val();
            var period = $('input[name="period"]').val();
            var mean_long = $('input[name="mean-longitude-degrees"]').val();

            if (isNumeric(a) && isNumeric(ecc) && isNumeric(asc_long) && isNumeric(inc) &&
                isNumeric(arg_per) && isNumeric(period) && isNumeric(mean_long) && validateDate(dates)) {
                //Send the post request

                $.ajax({
                    data: {
                        'semi-major-axis': a,
                        'eccentricity': ecc,
                        'ascending-node': asc_long,
                        'inclination': inc,
                        'periastron': arg_per,
                        'period': period,
                        'dates': dates,
                        'mean_long_degrees': mean_long
                    },
                    type: 'POST',
                    url: '/orbit_position_other'
                }).done(function (result) {
                    if (result.error == 0) {
                        let radius_vector = result.radius_vector;
                        let ra = result.RA;
                        let dec = result.DEC;
                        let res = `<p class="mt-2">The planet is at a distance of ${radius_vector} AU from its host star. Spherical coordinates are right ascention=${ra}, declination=${dec}. These are the positions in orbit with respect to the host star right now and will differ from the average values as not all orbits are circular.</p>`
                        $('#orbit-position-result').html(res);
                    } else {
                        let res = `<h6 class="mt-2 text-danger">Oops, something went wrong</h6>`;
                        $('#orbit-position-result').html(res);
                    }


                })

            } else {
                //Invalid input
                let res = `<h6 class="mt-2 text-danger">Invalid inputs</h6>`;
                $('#orbit-position-result').html(res);
            }

        });
    }
});


$("form[name='DistanceForm']").on('submit', function (event) {
    event.preventDefault();
    $.ajax({
        data: {
            PlanetName: $("input[name='PlanetName']").val()
        },
        type: 'POST',
        url: '/distance'

    }).done(function (data) {
        if (data.error == 0) {
            let distance = data.distance;
            let res = `<h6 class="mt-2">Estimated distance=${distance} parsecs</h6>`
            $('#result-calc-distance').html(res);
        } else {
            let res = `<h6 class="mt-2">Planet distance is not in the dataset</h6>`
            $('#result-calc-distance').html(res);
        }
    });
});



$('form[name="PeriodForm"]').on('submit', function (event) {
    event.preventDefault();
    let a = $('input[name="semi-major-axis-period"]').val();
    let slrmass = $('input[name="star-solar-mass"]').val();
    if (isNumeric(a) && isNumeric(slrmass)) {
        $.ajax({
            data: {
                'semi-major-axis': a,
                'mass': slrmass
            },
            type: 'POST',
            url: '/orbital_period'
        }).done(function (result) {
            let period = result.orbital_period;
            let res = `<p class="mt-2">Orbital period of the planet is ${period}</p>`;
            $('#orbital-period-result').html(res);
        });
    } else {
        let res = `<h6 class="mt-2 text-danger">Invalid inputs</h6>`;
        $('#orbital-period-result').html(res);

    }
});

$('input[name="dec-1"]').attr('placeholder', "DEC planet 1(\u00b1DD \u00b1MM \u00b1SS)");
$('input[name="dec-2"]').attr('placeholder', "DEC planet 2(\u00b1DD \u00b1MM \u00b1SS)");


$('form[name="angleForm"]').on('submit', function () {
    event.preventDefault();
    let ra_1 = $('input[name="ra-1"]').val();
    let ra_2 = $('input[name="ra-2"]').val();
    let dec_1 = $('input[name="dec-1"]').val();
    let dec_2 = $('input[name="dec-2"]').val();
    if (validateRA(ra_1) && validateRA(ra_2) && validateDEC(dec_1) && validateDEC(dec_2)) {

        $.ajax({
            data: {
                'ra_1': ra_1,
                'ra_2': ra_2,
                'dec_1': dec_1,
                'dec_2': dec_2
            },
            type: 'POST',
            url: '/angle'

        }).done(function (result) {

            let angle = result.angle;
            let res = `<h6 class="mt-2">Angle between the planets=${angle} &#176.`
            $('#angle-result').html(res);

        });


    } else {
        let res = `<h6 class="mt-2 text-danger">Invalid Inputs</h6>`;
        $('#angle-result').html(res);
    }

});


function validateRA(ra) {
    ra = ra.split(" ");
    if (ra.length != 3)
        return false;
    if (isNumeric(ra[0] && isNumeric(ra[1]) && isNumeric(ra[2])) && ra[0] > 0 && ra[1] > 0 && ra[2] > 0)
        return true;
    return false;
}

function validateDEC(dec) {
    dec = dec.split(' ');

    if (dec.length != 3)
        return false;
    if (isNumeric(dec[0]) && isNumeric(dec[1]) && isNumeric(dec[2]))
        return true;
    return false;
}

function validateDate(str) {
    var m = str.match(/^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{2}$/);
    return m;
}

function isNumeric(num) {
    if (num == '')
        return false
    else
        return !isNaN(num)
}

$('input[name="search-field"]').autocomplete({
    source: function (request, response) {
        console.log('Working!');
        $.ajax({
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            type: 'GET',
            data: {
                'query': $('input[name="search-field"]').val()
            },
            url: '/search_hints',

        }).done(function (data) {
            response(data);

            console.log(data)
        });
    },
    _renderItem: function (ul, item) {
        return $("<li class='ui-autocomplete'>")
            .attr("data-value", item.value)
            .append(item.label)
            .appendTo(ul);
    }
});


$('.carousel').carousel({
    interval: 2000
})
