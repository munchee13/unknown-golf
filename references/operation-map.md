# Unknown Golf API Operation Map

Generated from `openapi.json`.

| Tag | OperationId | Method | Path | Summary |
|---|---|---|---|---|
| Authentication | auth | POST | /v1/auth | Login |
| Community | search | GET | /v1/community/search | Search communities |
| Event | rounds | GET | /v1/events/{eventId}/rounds | List all rounds |
| Event | search_1 | GET | /v1/events | Search events |
| Event Courses | list | GET | /v1/events/{eventId}/courses | List all courses |
| Event Courses | tees | GET | /v1/events/{eventId}/courses/{courseId}/tees | List all course tees |
| Event Courses | tees_1 | GET | /v1/events/{eventId}/courses/{courseId}/tees/{teeId} | Retrieve course tee |
| Event Flights | assignPlayer | POST | /v1/events/{eventId}/flights/{flightId}/players/{playerId} | Assign player |
| Event Flights | assignTeam | POST | /v1/events/{eventId}/flights/{flightId}/teams/{teamId} | Assign team |
| Event Flights | deleteFlight | DELETE | /v1/events/{eventId}/flights/{flightId} | Delete flight |
| Event Flights | deleteFlightAll | DELETE | /v1/events/{eventId}/flights | Delete all flights |
| Event Flights | listLeaderboard | GET | /v1/events/{eventId}/flights/leaderboards/{leaderboardId} | List flights for leaderboard |
| Event Flights | listUnassignedPlayers | GET | /v1/events/{eventId}/flights/leaderboards/{leaderboardId}/unassigned/players | List players unassigned |
| Event Flights | listUnassignedTeams | GET | /v1/events/{eventId}/flights/leaderboards/{leaderboardId}/unassigned/teams | List teams unassigned |
| Event Flights | list_1 | GET | /v1/events/{eventId}/flights | List all flights |
| Event Flights | removePlayer | DELETE | /v1/events/{eventId}/flights/{flightId}/players/{playerId} | Remove player |
| Event Flights | removeTeam | DELETE | /v1/events/{eventId}/flights/{flightId}/teams/{teamId} | Remove team |
| Event Handicap (Player) | search_2 | GET | /v1/events/{eventId}/players/handicaps | Search handicaps |
| Event Handicap (Player) | updateByCoursePlaying | PATCH | /v1/events/{eventId}/players/{playerId}/handicap/coursePlaying | Update handicap |
| Event Handicap (Player) | updateByIndex | PATCH | /v1/events/{eventId}/players/{playerId}/handicap/index | Update handicap index |
| Event Handicap (Player) | updateLocked | PATCH | /v1/events/{eventId}/players/{playerId}/handicap/lock | Update locked |
| Event Handicap (Player) | updateLockedAll | PATCH | /v1/events/{eventId}/players/handicaps/lock | Update lock all |
| Event Handicap (Player) | updateTee | PATCH | /v1/events/{eventId}/players/{playerId}/handicap/tee/{teeId} | Update Assigned tee |
| Event Handicap (Team) | search_3 | GET | /v1/events/{eventId}/teams/handicaps | Search handicaps |
| Event Handicap (Team) | updateByCoursePlaying_1 | PATCH | /v1/events/{eventId}/teams/{teamId}/handicap | Update handicap |
| Event Handicap (Team) | updateLockedAll_1 | PATCH | /v1/events/{eventId}/teams/handicaps/lock | Update lock all |
| Event Handicap (Team) | updateLocked_1 | PATCH | /v1/events/{eventId}/teams/{teamId}/handicap/lock | Update locked |
| Event Leaderboards | list_2 | GET | /v1/events/{eventId}/leaderboards | List all leaderboards |
| Event Players | create | POST | /v1/events/{eventId}/players | Register player |
| Event Players | delete | DELETE | /v1/events/{eventId}/players/{playerId} | Remove player |
| Event Players | search_4 | GET | /v1/events/{eventId}/players | List all players |
| Event Scores (Player) | search_5 | GET | /v1/events/{eventId}/players/scores | Search scores |
| Event Scores (Team) | search_6 | GET | /v1/events/{eventId}/teams/scores | Search scores |
| Event Teams | add | POST | /v1/events/{eventId}/teams | Add team |
| Event Teams | assignPlayer_1 | POST | /v1/events/{eventId}/teams/{teamId}/players/{playerId} | Assign player |
| Event Teams | assignPlayers | POST | /v1/events/{eventId}/teams/players | Assign players |
| Event Teams | deleteAll | DELETE | /v1/events/{eventId}/teams | Delete all teams |
| Event Teams | delete_1 | DELETE | /v1/events/{eventId}/teams/{teamId} | Delete team |
| Event Teams | list_3 | GET | /v1/events/{eventId}/teams | List all teams |
| Event Teams | removeAllPlayers | DELETE | /v1/events/{eventId}/teams/players | Remove all players all teams |
| Event Teams | removePlayer_1 | DELETE | /v1/events/{eventId}/teams/{teamId}/players/{playerId} | Remove player |
| Event Teams | removePlayersAll | DELETE | /v1/events/{eventId}/teams/{teamId}/players | Remove players all |
| Event Teams | updateName | PATCH | /v1/events/{eventId}/teams/{teamId}/name/{name} | Update name |
| Event Tee Pairings | addTeeTime | POST | /v1/events/{eventId}/teePairings | Create tee pairings |
| Event Tee Pairings | assignPlayer_2 | POST | /v1/events/{eventId}/teePairings/{teePairingId}/players/{playerId} | Assign player |
| Event Tee Pairings | assignPlayersAll | POST | /v1/events/{eventId}/teePairings/players | Assign players |
| Event Tee Pairings | deleteTeeTime | DELETE | /v1/events/{eventId}/teePairings/{teePairingId} | Delete tee pairing |
| Event Tee Pairings | deleteTeeTimesAll | DELETE | /v1/events/{eventId}/teePairings | Delete all tee pairings |
| Event Tee Pairings | listAllRounds | GET | /v1/events/{eventId}/teePairings/allRounds | List tee pairings all rounds |
| Event Tee Pairings | list_4 | GET | /v1/events/{eventId}/teePairings | List tee pairings |
| Event Tee Pairings | removePlayer_2 | DELETE | /v1/events/{eventId}/teePairings/{teePairingId}/players/{playerId} | Remove player |
| Event Tee Pairings | removePlayersAll_1 | DELETE | /v1/events/{eventId}/teePairings/players | Remove all players |
| Event Tee Pairings | updateTeeTime | PUT | /v1/events/{eventId}/teePairings | Update tee pairings |
| Event Web Links | linkFlightList | GET | /v1/events/{eventId}/weblinks/flights | Flights list |
| Event Web Links | linkPlayersList | GET | /v1/events/{eventId}/weblinks/players | Players list |
| Event Web Links | linkPlayersScore | GET | /v1/events/{eventId}/weblinks/players/{playerId}/scoring | Player enter scores |
| Event Web Links | linkPlayersScoreAny | GET | /v1/events/{eventId}/weblinks/players/scoring | Player (any) enter scores |
| Event Web Links | linkPlayersSignUp | GET | /v1/events/{eventId}/weblinks/players/{playerId}/register | Player registration |
| Event Web Links | linkPlayersSignUpPublic | GET | /v1/events/{eventId}/weblinks/players/public/register | Player public registration |
| Event Web Links | linkResults | GET | /v1/events/{eventId}/weblinks/results | Results list |
| Event Web Links | linkTeamList | GET | /v1/events/{eventId}/weblinks/teams | Teams list |
| Event Web Links | linkTeeSheet | GET | /v1/events/{eventId}/weblinks/teeSheet | Tee sheet list |
| Player | addToCommunity | POST | /v1/players/{playerId}/communities/{communityId} | Add player to community |
| Player | create_1 | POST | /v1/players | Create player |
| Player | deleteFromCommunity | DELETE | /v1/players/{playerId}/communities/{communityId} | Remove player from community |
| Player | listCommunities | GET | /v1/players/{playerId}/communities | list player communities |
| Player | search_7 | GET | /v1/players | Search players |
| Player | udpateEmail | PATCH | /v1/players/{playerId}/email | Update email |
| Player | udpateMemberStatus | PATCH | /v1/players/{playerId}/communities/{communityId}/member | Update member status |
| Player | updateDateOfBirth | PATCH | /v1/players/{playerId}/dob | Update date of birth |
| Player | updateHandicapId | PATCH | /v1/players/{playerId}/handicap | Update handicap id |
| Player | updateHandle | PATCH | /v1/players/{playerId}/communities/{communityId}/handle | Update handle |
| Player | updateName_1 | PATCH | /v1/players/{playerId}/name | Update name |
| Player | updatePhoneNumber | PATCH | /v1/players/{playerId}/phone | Update phone number |
| Untagged | getExternalGrammar | GET | /v1/application.wadl/{path} |  |
| Untagged | getWadl | GET | /v1/application.wadl |  |
| Utility | hcProviders | GET | /v1/util/worldHandicaps/providers | World Handicap Providers |
| Utility | list_5 | GET | /v1/util/leaderboards/types | List all leaderboard types |