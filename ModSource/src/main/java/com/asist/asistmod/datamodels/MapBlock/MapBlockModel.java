package com.asist.asistmod.datamodels.MapBlock;

import com.opencsv.bean.CsvBindByName;
import com.opencsv.bean.MappingStrategy;

public class MapBlockModel  {
    @CsvBindByName(column = "LocationXYZ")
    private String locationXYZ;

    public void setLocationXYZ(String locationXYZ) {
        this.locationXYZ = locationXYZ;
    }
     
    public String getLocationXYZ() {
        return this.locationXYZ.trim();
    }
    
    @CsvBindByName(column = "BlockType")
    private String blockType;

    public String getBlockType() {
		return blockType;
	}

	public void setBlockType(String blockType) {
		this.blockType = blockType.trim();
	}

	@CsvBindByName(column = "Command")
    private String command;

	public String getCommand() {
		return command;
	}

	public void setCommand(String command) {
		this.command = command.trim();
	}

    @CsvBindByName(column = "CommandOptions")
    private String commandOption;

	public String getCommandOptions() {
		return commandOption;
	}

	public void setCommandOption(String commandOption) {
		this.commandOption = commandOption.trim();
	}

    @CsvBindByName(column = "RoomName")
    private String roomname;

	public String getRoomName() {
		return roomname;
	}

	public void setRoomName(String roomname) {
		this.roomname = roomname.trim();
	}

	@CsvBindByName(column = "FeatureType")
    private String featureType;

	public String getFeatureType() {
		return featureType;
	}

	public void setFeatureType(String featureType) {
		this.featureType = featureType.trim();
	}
}