package com.asist.asistmod.GuiOverlays.TestGui;

import com.asist.asistmod.missionhelpers.timer.MissionTimerListener;

import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.Gui;
import net.minecraft.client.gui.ScaledResolution;
import net.minecraft.client.renderer.GlStateManager;

import org.lwjgl.LWJGLException;
import org.lwjgl.opengl.GLContext;

public class TestGui extends Gui  {
	
	Minecraft mc;
	ScaledResolution resolution;
	
	int width;	
	int height;
	
	public static int maxTeamScore = 0;	
	public static int teamScore = 0;
	
	public static int regularVictimsSaved = 0;
	public static int maxRegularVictims = 0;
	
	public static int criticalVictimsSaved = 0;
	public static int maxCriticalVictims = 0;
	
	public static int victimCount = 0;
	public static int minute = 0;
	public static int second = 0;
	
	public static float scaleFactor = 0.75f;
	
	int actualScaledWidth;
	int actualScaledHeight;			
	
	int widthScaledBackTo1;
	int heightScaledBackTo1;
	
	public TestGui(Minecraft mc)
	
	{
		
		this.mc = mc;
		this.resolution = new ScaledResolution(mc);
		this.width = resolution.getScaledWidth();
		this.height = resolution.getScaledHeight();	
		
		this.setScaling();
		
		// probably just want to draw this after instatiating a single gui object in RenderGuiHandler
		draw();
		
	}
	
	public void setScaling() {
		this.actualScaledWidth = (int) (width * scaleFactor);
		this.actualScaledHeight = (int) (height * scaleFactor);			
		
		this.widthScaledBackTo1 = (int)(width * (1/scaleFactor) );
		this.heightScaledBackTo1 = (int)(height * (1/scaleFactor) );
	}
	
	public void draw(  ) {
		
		try {
			//System.out.println("Drawing.");
			GLContext.useContext(mc);
			
			this.setScaling();
			
			GlStateManager.pushMatrix();
			// This is a transformation matrix, so all referenced width and height values within the pushMatrix and popMatrix Commands can be considered scaled to the
			// degree below. You cannot get this scaled value by accessing the width and height variable, as it seems they are transformed AFTER being passed to drawString
			// hence the "scaledBackTo1 variables -> which are the UNSCALED coordinates of where to place SCALED strings ... confusing I know
			
			GlStateManager.scale(scaleFactor, scaleFactor, scaleFactor);	
			
			// TIMER LABEL
			//drawString(mc.fontRendererObj, "Timer", (int)( widthScaledBackTo1 - ( widthScaledBackTo1 * .16 ) ), (int)( heightScaledBackTo1 - (heightScaledBackTo1*0.6) ), Integer.parseInt("03C838", 16));
			this.drawAtPosition("Timer", 0.2f, 0.6f, "2AE311");
			// VICTIM LABEL
			//drawString(mc.fontRendererObj, "Victims", (int)(widthScaledBackTo1-(widthScaledBackTo1 * .16)), (int)( heightScaledBackTo1 - (heightScaledBackTo1*0.55) ), Integer.parseInt("F2FF22", 16));
			this.drawAtPosition("Regular", 0.2f, 0.55f, "D7E311");
			//TEAMSCORE LABEL
			//drawString(mc.fontRendererObj, "TeamScore", (int)(widthScaledBackTo1-(widthScaledBackTo1 * .16)), (int)( heightScaledBackTo1 - (heightScaledBackTo1*0.50) ), Integer.parseInt("D51669", 16));
			this.drawAtPosition("Critical", 0.2f, 0.50f, "E32711");
			
			this.drawAtPosition("Team", 0.2f, 0.45f, "11DFE3");
			
			// TIMER VALUE
			//drawString(mc.fontRendererObj, getTimeString(), (int)( widthScaledBackTo1 - ( widthScaledBackTo1 * .06 ) ), (int)( heightScaledBackTo1 - (heightScaledBackTo1*0.6) ), Integer.parseInt("FFFFFF", 16));
			this.drawAtPosition(getTimeString(), 0.1f, 0.60f, "FFFFFF");	
			// VICTIM VALUE
			//drawString(mc.fontRendererObj, Integer.toString(victimCount), (int)( widthScaledBackTo1 - ( widthScaledBackTo1 * .06 ) ), (int)( heightScaledBackTo1 - (heightScaledBackTo1*0.55) ), Integer.parseInt("FFFFFF", 16));
			this.drawAtPosition(getRegularVictimsText(), 0.1f, 0.55f, "FFFFFF");
			
			this.drawAtPosition(getCriticalVictimsText(), 0.1f, 0.50f, "FFFFFF");
			// TEAMSCORE VALUE
			//drawString(mc.fontRendererObj, Integer.toString(teamScore), (int)( widthScaledBackTo1 - ( widthScaledBackTo1 * .06 ) ), (int)( heightScaledBackTo1 - (heightScaledBackTo1*0.50) ), Integer.parseInt("FFFFFF", 16));
			this.drawAtPosition(getTeamScoreText(), 0.1f, 0.45f, "FFFFFF");
			
			GlStateManager.popMatrix();
			
			//System.out.println("TestGui Time : " + getTimeString());
			
			//System.out.println("TestGui Victim Count : " + victimCount);
		
		} catch (LWJGLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		
	}
	
	public void drawAtPosition(String value, float xFloatPercentFromRight, float yFloatPercentFromTop, String colorCode) {
		
		drawString(mc.fontRendererObj, value, (int)( widthScaledBackTo1 - ( widthScaledBackTo1 * xFloatPercentFromRight ) ), (int)( heightScaledBackTo1 - (heightScaledBackTo1*yFloatPercentFromTop) ), Integer.parseInt(colorCode, 16));
		
	}
	
	public String getTimeString() {
		
		StringBuilder sb = new StringBuilder("");
		
		// MINUTE
		if ( this.minute < 10) {			
			sb.append(Integer.toString(0));						
		}
		
		sb.append(Integer.toString(minute));
		sb.append(":");
		
		// SECOND
		if ( this.second < 10) {			
			sb.append(Integer.toString(0));						
		}
		
		sb.append(Integer.toString(second));
		
		
		return sb.toString();
	}
	
	private String getRegularVictimsText() {
		
		StringBuilder sb = new StringBuilder();
		
		sb.append( Integer.toString(this.regularVictimsSaved));
		sb.append("/");
		sb.append(Integer.toString(this.maxRegularVictims));
		
		return sb.toString();
	}
	
	private String getCriticalVictimsText() {
		
		StringBuilder sb = new StringBuilder();
		
		sb.append( Integer.toString(this.criticalVictimsSaved));
		sb.append("/");
		sb.append(Integer.toString(this.maxCriticalVictims));
		
		return sb.toString();
	}
	
	private String getTeamScoreText() {
		
		StringBuilder sb = new StringBuilder();
		
		sb.append( Integer.toString(this.teamScore));
		sb.append("/");
		sb.append(Integer.toString(this.maxTeamScore));
		
		return sb.toString();
	}
	
	
	public void onVictimCountChange ( int vc) {
		
		victimCount = vc;
	}
	
	public void onMissionTimeChange (int m, int s) {
		
		minute = m;
		second = s;		
	
	}
	
	public void onTeamScoreChange (int s) {		
		teamScore = s;
	
	}
	
	public void onScoreboardChange (int rvs,int mrv, int cvs, int mcv, int ts, int mts) {		
		
		this.regularVictimsSaved = rvs;
		this.maxRegularVictims = mrv;
		this.criticalVictimsSaved = cvs;
		this.maxCriticalVictims = mcv;
		this.teamScore = ts;
		this.maxTeamScore = mts;
	
	}
}
