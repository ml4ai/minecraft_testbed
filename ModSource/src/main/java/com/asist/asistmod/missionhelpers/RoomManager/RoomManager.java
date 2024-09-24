package com.asist.asistmod.missionhelpers.RoomManager;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

import com.asist.asistmod.datamodels.PositionRange.PositionRangeModel;
import com.asist.asistmod.datamodels.TrialInfo.TrialInfoModel;

import com.google.gson.Gson;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.stream.JsonReader;

import net.minecraft.util.math.BlockPos;

public class RoomManager {
	
	public static Map<String,RoomDefinition> room_defs = new HashMap<String,RoomDefinition>();

	public RoomManager() {
		// TODO Auto-generated constructor stub
	}
	
	public static void readInRoomDefs(String filename) {
		
		FileReader fileReader;
		try {
			fileReader = new FileReader("./mods/"+filename);
			JsonReader jr = new JsonReader(fileReader);
			jr.setLenient(true);			
			Gson gson = new Gson();
			JsonObject jsonObject = gson.fromJson(jr, JsonObject.class);			
			
	        Set<Entry<String, JsonElement>> entrySet = jsonObject.entrySet();

			entrySet.forEach(entry -> {
				System.out.println(entry.getKey());
				JsonObject val = entry.getValue().getAsJsonObject();
				int min_x = val.get("min_x").getAsInt();
				int min_z = val.get("min_z").getAsInt();
				int max_x = val.get("max_x").getAsInt();
				int max_z = val.get("max_z").getAsInt();
				room_defs.put(entry.getKey(), new RoomDefinition(min_x,min_z,max_x,max_z));
			
			});
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		
	}
	
	public static void printRoomDefs() {
		room_defs.forEach((k,v)->{
			System.out.println("Room : " + k );
			System.out.println("Min Z : " + v.min_z);
			System.out.println("Min X : " + v.min_x);
			System.out.println("Max Z : " + v.max_z);
			System.out.println("Max X : " + v.max_x);
		});
	}
	
}
