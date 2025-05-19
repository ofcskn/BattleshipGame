# Battleship Game Protocol

This protocol defines the commands exchanged between the **client** and **server** in the **Board&Socket-Based Battleship Multiplayer Game**. Communication is command-based using predefined string constants.

## Client → Server Commands

| Command                                   | Description                                                                               |
| ----------------------------------------- | ----------------------------------------------------------------------------------------- |
| `CLIENT_COMMAND_PING`                     | Send a ping to the server to check the connection status.                                 |
| `CLIENT_COMMAND_FIND_OPPONENT`            | Request to find an available opponent to start a match.                                   |
| `CLIENT_COMMAND_OPPONENT_RIGHT_TO_ATTACK` | Inform the server that the **opponent**, not the current client, has the right to attack. |
| `CLIENT_COMMAND__CANCEL_FIND_OPPONENT`    | Cancel the search for an opponent (before a match is found).                              |

---

## Server → Client Commands

| Command                                     | Description                                                                |
| ------------------------------------------- | -------------------------------------------------------------------------- |
| `SERVER_COMMAND_PING`                       | Server response to `CLIENT_COMMAND_PING`, confirms connection is alive.    |
| `SERVER_COMMAND_FOUND_OPPONENT`             | Match found — game can begin. Sent to both matched players.                |
| `SERVER_COMMAND_NOT_MATCHED`                | No opponent is available to match at the moment. Try again later.          |
| `SERVER_COMMAND_ATTACK_TURN`                | Notify the client that the player is performing an attack move.            |
| `SERVER_COMMAND_ATTACK_BLOCK`               | Indicates a player has attacked a block (square) on opponent’s board.      |
| `SERVER_COMMAND_OPPONENT_IS_ATTACKED_BLOCK` | Notify the opponent that their ship/block has been attacked.               |
| `SERVER_COMMAND_RIGHT_TO_ATTACK`            | Grants the player the right to attack in this turn.                        |
| `SERVER_COMMAND_OPPONENT_RIGHT_TO_ATTACK`   | Informs the player that it's the opponent’s turn to attack.                |
| `SERVER_COMMAND_LEFT_MATCH`                 | Informs the player that their opponent has left the match or disconnected. |

---

## Example Flow

1. **Client** sends `CLIENT_COMMAND_FIND_OPPONENT`.
2. **Server** responds with:

   - `SERVER_COMMAND_FOUND_OPPONENT` → match started, or
   - `SERVER_COMMAND_NOT_MATCHED` → keep waiting or retry.

3. Game turn begins:

   - Server sends `SERVER_COMMAND_RIGHT_TO_ATTACK` to Player A.
   - Player A attacks with `SERVER_COMMAND_ATTACK_TURN`.
   - Server responds with:

     - `SERVER_COMMAND_ATTACK_BLOCK` to Player A
     - `SERVER_COMMAND_OPPONENT_IS_ATTACKED_BLOCK` to Player B

4. If Player B’s turn, server sends `SERVER_COMMAND_OPPONENT_RIGHT_TO_ATTACK`.

---
