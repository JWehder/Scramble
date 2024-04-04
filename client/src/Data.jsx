// some of the values will need to be updated during the tourney


// avgScore is null initially until we calculate it
// possibility that we will need to determine this field after every tourney/ cut
const player = {
    firstName: "Scottie",
    lastName: "Scheffler",
    Age: 26,
    Country: "USA",
    pgaDebut: 2018,
    swings: "R",
    weight: 200,
    college: "University of Texas",
    cuts: 3,
    cutsMade: 2,
    earnings: "$72441",
    events_played: 1,
    first_place: 0,
    second_place: 0,
    third_place: 0,
    top_10: 0,
    top_25: 0,
    cuts: 0,
    cuts_made: 1,
    withdrawals: 0,
    points: 12,
    points_rank: 188,
    earnings: 21480,
    earnings_rank: 193,
    drive_avg: 293.6,
    drive_acc: 60.71,
    gir_pct: 72.22,
    putt_avg: 1.731,
    sand_saves_pct: 50,
    birdies_per_round: 4.25,
    world_rank: 531,
    scrambling_pct:75,
    scoring_avg: 71.225,

}

// cutLine will be an updated field for each day of the tourney
const tournament = {
    tournamentName: "The Masters",
    date: "12/04/24",
    location: "Somewhere, GA",
    fieldCount: 102,
    cutLine: -2
}

const courses = [
    {
      id: "7e9462a5-66ea-4205-b37a-81884e3653cf",
      name: "Augusta National",
      yardage: 7510,
      par: 72,
      holes: [
        {
          sequence: 1,
          number: 1,
          par: 4,
          strokes: 385,
          players: 90,
          eagles: 0,
          birdies: 6,
          pars: 57,
          bogeys: 23,
          double_bogeys: 4,
          holes_in_one: 0,
          other_scores: 0,
          strokes_avg: 4.28,
          avg_diff: 0.28
        },
        {
          sequence: 2,
          number: 2,
          par: 5,
          strokes: 422,
          players: 90,
          eagles: 0,
          birdies: 37,
          pars: 44,
          bogeys: 9,
          double_bogeys: 0,
          holes_in_one: 0,
          other_scores: 0,
          strokes_avg: 4.69,
          avg_diff: -0.31
        }
      ]
    }
]

// have a matchup randomized generator
// rivalries
const league = {
    name: "league",
    type: "Stroke Play",
    user: "Tom Sanderson",
    users: [{}],
    teams: [{}],
    tournaments: [],
    maxAmountOfTeams: 8,
    public: false,
    rivalries: [{}]
}

const event = {
    type: "draft",
    name: "name of league draft",
    league: {}
}

const user = {
    username: "username",
    password: "password",
    passwordConfirmation: "password confirmation",
    leagues: [{}],
    teams: [{}],
    email: "email",
    phone: 6145618040,
}

const game = {
    name: "Stroke Play",
    matchups: false,
    icon: "icon.png",
    description: "description",
    maxNumberOfUsers: 14,
    starterThreshold: 3,
    benchThreshold: 2
}

{
    "tour": {
      "id": "b52068af-28e4-4e91-bdbb-037591b0ff84",
      "alias": "pga",
      "name": "PGA Tour"
    },
    "season": {
      "id": "55827590-93f7-4493-9b4f-83ae86116ef6",
      "year": 2024
    },
    "tournaments": [
      {
        "id": "c03e44a6-a71d-433e-86be-e28506ffcec1",
        "name": "The Sentry",
        "event_type": "stroke",
        "purse": 20000000,
        "winning_share": 3600000,
        "currency": "USD",
        "points": 700,
        "start_date": "2024-01-04",
        "end_date": "2024-01-07",
        "course_timezone": "Pacific/Honolulu",
        "network": "Golf Channel",
        "total_rounds": 4,
        "status": "closed",
        "defending_champ": {
          "id": "7b52b9be-a490-4569-9bbc-57db5f232dcb",
          "first_name": "Jon",
          "last_name": "Rahm",
          "height": 74,
          "weight": 220,
          "birthday": "1994-11-10",
          "country": "SPAIN",
          "residence": "Scottsdale, AZ, USA",
          "birth_place": "Barrika,, ESP",
          "college": "Arizona State",
          "turned_pro": 2016,
          "handedness": "R",
          "abbr_name": "J.Rahm"
        },
        "winner": {
          "id": "e4f92dca-86d5-441e-8a2d-55d5360937c5",
          "first_name": "Chris",
          "last_name": "Kirk",
          "height": 75,
          "weight": 175,
          "birthday": "1985-05-08T00:00:00+00:00",
          "country": "UNITED STATES",
          "residence": "St. Simons Island, GA, USA",
          "birth_place": "Knoxville, TN, USA",
          "college": "Georgia",
          "turned_pro": 2007,
          "handedness": "R",
          "abbr_name": "C.Kirk",
          "name": "Kirk, Chris"
        },
        "venue": {
          "id": "4e353af5-a1dd-4118-963d-24ef08393155",
          "name": "Kapalua Resort",
          "city": "Kapalua",
          "state": "HI",
          "zipcode": "96761",
          "country": "USA",
          "courses": [
            {
              "id": "f14b3a94-b487-448d-bb1c-a4a77aa4523d",
              "name": "The Plantation Course at Kapalua Resort",
              "yardage": 7596,
              "par": 73,
              "holes": [
                {
                  "number": 1,
                  "par": 4,
                  "yardage": 520
                },
                {
                  "number": 2,
                  "par": 3,
                  "yardage": 219
                },
                {
                  "number": 3,
                  "par": 4,
                  "yardage": 424
                },
                {
                  "number": 4,
                  "par": 4,
                  "yardage": 422
                },
                {
                  "number": 5,
                  "par": 5,
                  "yardage": 526
                },
                {
                  "number": 6,
                  "par": 4,
                  "yardage": 424
                },
                {
                  "number": 7,
                  "par": 4,
                  "yardage": 522
                },
                {
                  "number": 8,
                  "par": 3,
                  "yardage": 199
                },
                {
                  "number": 9,
                  "par": 5,
                  "yardage": 550
                },
                {
                  "number": 10,
                  "par": 4,
                  "yardage": 384
                },
                {
                  "number": 11,
                  "par": 3,
                  "yardage": 161
                },
                {
                  "number": 12,
                  "par": 4,
                  "yardage": 424
                },
                {
                  "number": 13,
                  "par": 4,
                  "yardage": 383
                },
                {
                  "number": 14,
                  "par": 4,
                  "yardage": 301
                },
                {
                  "number": 15,
                  "par": 5,
                  "yardage": 541
                },
                {
                  "number": 16,
                  "par": 4,
                  "yardage": 369
                },
                {
                  "number": 17,
                  "par": 4,
                  "yardage": 550
                },
            ]
