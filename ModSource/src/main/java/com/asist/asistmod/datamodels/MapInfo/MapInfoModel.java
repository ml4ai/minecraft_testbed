package com.asist.asistmod.datamodels.MapInfo;

import com.opencsv.bean.CsvBindByName;
import com.opencsv.bean.MappingStrategy;

public class MapInfoModel  {
    @CsvBindByName(column = "LocationXYZ")
    private String locationXYZ;

    public void setLocationXYZ(String locationXYZ) {
        this.locationXYZ = locationXYZ;
    }
     
    public String getLocationXYZ() {
        return this.locationXYZ.trim();
    }
    
    @CsvBindByName(column = "FeatureType")
    private String featureType;

    public String getFeatureType() {
		return featureType;
	}

	public void setFeatureType(String featureType) {
		this.featureType = featureType.trim();
	}

	@CsvBindByName(column = "FeatureSubType")
    private String featureSubType;

	public String getFeatureSubType() {
		return featureSubType;
	}

	public void setFeatureSubType(String featureSubType) {
		this.featureSubType = featureSubType.trim();
	}

    @CsvBindByName(column = "RoomName")
    private String roomname;

	public String getRoomName() {
		return roomname;
	}

	public void setRoomName(String roomname) {
		this.roomname = roomname.trim();
	}
}