package com.asist.asistmod.datamodels.ModSettings;

public class SafeZone {
	
	public int minX = 10000;
	public int maxX= 10000;
	public int minZ = 10000;
	public int maxZ = 10000;	
	
	public void printDetails() {
		System.out.println(	minX + " <-X-> " + maxX );
		System.out.println(	minZ + " <-Z-> " + maxZ );
	}
}