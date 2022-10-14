import pickle

logos = {
    1: "https://cms.nhl.bamgrid.com/images/assets/binary/301891622/binary-file/file.svg"
    ,2: "https://cms.nhl.bamgrid.com/images/assets/binary/316482732/binary-file/file.svg"
    ,3: "https://cms.nhl.bamgrid.com/images/assets/binary/289471614/binary-file/file.svg"
    ,4: "https://www-league.nhlstatic.com/images/logos/teams-current-primary-light/4.svg"
    ,5: "https://www-league.nhlstatic.com/images/logos/teams-current-primary-light/5.svg"
    ,6: "https://cms.nhl.bamgrid.com/images/assets/binary/301172494/binary-file/file.svg"
    ,7: "https://cms.nhl.bamgrid.com/images/assets/binary/318303268/binary-file/file.svg"
    ,8: "https://cms.nhl.bamgrid.com/images/assets/binary/309964716/binary-file/file.svg"
    ,9: "https://cms.nhl.bamgrid.com/images/assets/binary/319086486/binary-file/file.svg"
    ,10: "https://www-league.nhlstatic.com/images/logos/teams-current-primary-light/10.svg"
    ,12: "https://www-league.nhlstatic.com/nhl.com/builds/site-core/1b0537abbccc0707356f2da3f3f794e06472cbf3_1636047209/images/logos/team/current/team-12-dark.svg"
    ,13: "https://cms.nhl.bamgrid.com/images/assets/binary/291015530/binary-file/file.svg"
    ,14: "https://upload.wikimedia.org/wikipedia/en/thumb/2/2f/Tampa_Bay_Lightning_Logo_2011.svg/1200px-Tampa_Bay_Lightning_Logo_2011.svg.png"
    ,15: "https://cms.nhl.bamgrid.com/images/assets/binary/298789884/binary-file/file.svg"
    ,16: "https://cms.nhl.bamgrid.com/images/assets/binary/301971744/binary-file/file.svg"
    ,17: "https://www-league.nhlstatic.com/images/logos/teams-current-primary-light/17.svg"
    ,18: "https://www-league.nhlstatic.com/nhl.com/builds/site-core/1b0537abbccc0707356f2da3f3f794e06472cbf3_1636047209/images/logos/team/current/team-18-dark.svg"
    ,19: "https://cms.nhl.bamgrid.com/images/assets/binary/309991890/binary-file/file.svg"
    ,20: "https://cms.nhl.bamgrid.com/images/assets/binary/319279210/binary-file/file.svg"
    ,21: "https://www-league.nhlstatic.com/images/logos/teams-current-primary-dark/21.svg"
    ,22: "https://cms.nhl.bamgrid.com/images/assets/binary/290013862/binary-file/file.svg"
    ,23: "https://cms.nhl.bamgrid.com/images/assets/binary/309954422/binary-file/file.svg"
    ,24: "https://cms.nhl.bamgrid.com/images/assets/binary/299423002/binary-file/file.svg"
    ,25: "https://cms.nhl.bamgrid.com/images/assets/binary/325914394/binary-file/file.svg"
    ,26: "https://cms.nhl.bamgrid.com/images/assets/binary/308180580/binary-file/file.svg"
    ,28: "https://cms.nhl.bamgrid.com/images/assets/binary/301041748/binary-file/file.svg"
    ,29: "https://www-league.nhlstatic.com/images/logos/teams-current-primary-dark/29.svg"
    ,30: "https://www-league.nhlstatic.com/images/logos/teams-current-primary-light/30.svg"
    ,52: "https://www-league.nhlstatic.com/nhl.com/builds/site-core/1b0537abbccc0707356f2da3f3f794e06472cbf3_1636047209/images/logos/team/current/team-52-dark.svg"
    ,53: "https://cms.nhl.bamgrid.com/images/assets/binary/309994320/binary-file/file.svg"
    ,54: "https://cms.nhl.bamgrid.com/images/assets/binary/290581542/binary-file/file.svg"
    ,55: "https://cms.nhl.bamgrid.com/images/assets/binary/317578370/binary-file/file.svg"
}

if __name__ == "__main__":

    with open("./data/teamLogos.pkl", "wb") as file:
        pickle.dump(logos, file)