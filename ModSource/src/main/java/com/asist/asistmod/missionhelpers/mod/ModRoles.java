package com.asist.asistmod.missionhelpers.mod;

import com.asist.asistmod.missionhelpers.enums.RoleType;

import net.minecraft.block.state.IBlockState;

public class ModRoles {

	public static RoleType getEnumFromName(String roleName) {
		for(RoleType roleType : RoleType.values()) {
			if(roleType.getName().equals(roleName)) { return roleType; }
		}
		return RoleType.NULL;
	}
}
