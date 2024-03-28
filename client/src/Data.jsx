// some of the values will need to be updated during the tourney


// avgScore is null initially until we calculate it
// possibility that we will need to determine this field after every tourney/ cut
const player = {
    firstName: "Scottie",
    lastName: "Scheffler",
    avgScore: null,
    pgaDebut: 2018,
    tournaments: [{}],
}

// cutLine will be an updated field for each day of the tourney
const tournament = {
    tournamentName: "The Masters",
    date: "12/04/24",
    location: "Somewhere, GA",
    fieldCount: 102,
    cutLine: -2
}

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

