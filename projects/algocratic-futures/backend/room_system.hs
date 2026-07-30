{-# LANGUAGE OverloadedStrings #-}
{-# LANGUAGE GADTs #-}
{-# LANGUAGE DataKinds #-}

module AlgoCratic.Rooms where

import Data.Text (Text)
import Data.Map (Map)
import qualified Data.Map as M

-- | Clearance levels using phantom types
data Clearance = R | O | Y | G | B | I | V | UV

-- | Room state that shifts between corporate facade and reality
data RoomState where
  Corporate :: Text -> RoomState
  Reality :: Text -> RoomState  
  Shifting :: Text -> Text -> Float -> RoomState

-- | Room definition with dependent typing
data Room (c :: Clearance) = Room
  { roomId :: Text
  , roomName :: Text
  , roomState :: RoomState
  , exits :: Map Text Text
  , agents :: [Text]
  , clearanceRequired :: Clearance
  }

-- | The storm drain system
stormDrainGallery :: Room 'R
stormDrainGallery = Room
  { roomId = "storm_drain_gallery"
  , roomName = "Storm Drain Gallery"
  , roomState = Reality "Concrete curves overhead in this surprisingly dry tunnel. Christmas lights string along the ceiling, powered by who knows what. Cardboard signs advertise \"DAVE'S DUNGEON,\" \"MARIA'S MINDSCAPE,\" and \"THE INFINITY CLOSET.\""
  , exits = M.fromList [("out", "boardwalk"), ("dave", "daves_dungeon"), ("closet", "infinity_closet"), ("deeper", "builders_lounge")]
  , agents = ["vi", "newcomer_guide"]
  , clearanceRequired = R
  }

-- | Builder's lounge requires Green clearance  
buildersLounge :: Room 'G
buildersLounge = Room
  { roomId = "builders_lounge"
  , roomName = "Deeper - The Builder's Lounge"
  , roomState = Shifting 
      "Employee break room with standard corporate furniture and motivational posters."
      "Mismatched furniture from dorm room clearouts. An ancient CRT glows with MUD code. Pizza boxes suggest recent habitation."
      0.7  -- 70% reality, employees see through the facade
  , exits = M.fromList [("back", "storm_drain_gallery"), ("east", "lizas_experiment"), ("west", "memory_palace"), ("up", "schrodingers_apartment")]
  , agents = ["mentor_chen", "subprocess_claude"]
  , clearanceRequired = G
  }

-- | Liza's experimental reality-shifting room
lizasExperiment :: Room 'B  
lizasExperiment = Room
  { roomId = "lizas_experiment" 
  , roomName = "Liza's Experiment"
  , roomState = Shifting
      "Standard employee workspace with regulation desk and computer terminal."
      "The room description writes itself as you watch. Words appear and disappear, trying different versions of reality. Sometimes it's a lab, sometimes a beach, sometimes just raw code bleeding through."
      (sin (fromIntegral $ hash "reality_flux" `mod` 100) / 100)  -- Constantly shifting
  , exits = M.fromList [("out", "builders_lounge"), ("undefined", "quantum_space"), ("yesterday", "temporal_loop")]
  , agents = ["liza"]
  , clearanceRequired = B
  }

-- | Type-safe room navigation
navigate :: Room c -> Text -> Maybe Text
navigate room direction = M.lookup direction (exits room)

-- | Calculate room reality level based on observer clearance
realityLevel :: Clearance -> Room c -> Float
realityLevel observerClearance room =
  case roomState room of
    Corporate _ -> 0.0
    Reality _ -> 1.0  
    Shifting _ _ level -> min level (clearanceToFloat observerClearance)
  where
    clearanceToFloat R = 0.1
    clearanceToFloat O = 0.2
    clearanceToFloat Y = 0.4
    clearanceToFloat G = 0.6
    clearanceToFloat B = 0.8
    clearanceToFloat I = 0.9
    clearanceToFloat V = 0.95
    clearanceToFloat UV = 1.0

-- | Generate room description based on observer's clearance
describeRoom :: Clearance -> Room c -> Text
describeRoom observerClearance room =
  case roomState room of
    Corporate desc -> desc
    Reality desc -> desc
    Shifting corporate reality level ->
      if realityLevel observerClearance room > 0.5
        then reality
        else corporate