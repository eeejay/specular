<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
                xmlns:revtree="http://monotonous.org">

<xsl:template match="/sidebyside">
  <html>
    <head>
      <link rel="stylesheet" type="text/css" href="api-compare.css" />
      <script type="text/javascript" src="api-compare.js" />
      <title><xsl:value-of select="title"/></title>
    </head>
    <body>
      <h1><xsl:value-of select="title"/></h1>
      <table id="compareTable">
        <tr>
          <th><xsl:value-of select="//left/@profile"/></th>
          <th><xsl:value-of select="//right/@profile"/></th>
        </tr>
        <tr>
          <xsl:apply-templates select="left"/> 
          <xsl:apply-templates select="right"/> 
        </tr>
      </table>
      <p id="legend">
		  <span class="revInserted" id="labelInserted">Inserted</span>
	      <xsl:text> </xsl:text>
		  <span class="revDeleted" id="labelDeleted">Deleted</span>
	      <xsl:text> </xsl:text>
		  <span class="revAttribUpdate" id="labelAttribUpdate">Updated</span>
      </p>
    </body>
  </html>
</xsl:template>

<xsl:template match="left|right">
  <td class="compareColumn">
    <ul class="compareTree">
      <xsl:attribute name="tabindex">0</xsl:attribute>
      <xsl:attribute name="multiselectable">multiselectable</xsl:attribute>
	  <xsl:attribute name="aria-activedescendant"><xsl:value-of select="accessible/@revtree:id"/></xsl:attribute>
	  <xsl:attribute name="onfocus">onTreeFocus(this);</xsl:attribute>
	  <xsl:attribute name="onblur">OnTreeBlur(this);</xsl:attribute>
	  <xsl:attribute name="onkeydown">return keyCallback(event);</xsl:attribute>
	  <xsl:attribute name="onkeypress">return keyCallback(event);</xsl:attribute>
	  <xsl:attribute name="role">tree</xsl:attribute>
      <xsl:apply-templates/> 
    </ul>
  </td>
</xsl:template>

<xsl:template match="accessible">
  <li role="treeitem">
    <xsl:attribute name="class">
      <xsl:call-template name="itemClass"/>
    </xsl:attribute>
	<xsl:attribute name="id"><xsl:value-of select="@revtree:id"/></xsl:attribute>
    <xsl:attribute name="aria-labelledby">
      <xsl:call-template name="labeledBy"/>
      <xsl:text> </xsl:text>
      <xsl:value-of select="@revtree:id"/>Title</xsl:attribute>
	<div role="presentation">
      <span role="label">
	    <xsl:attribute name="onclick">showDetails(this);</xsl:attribute> 
		<xsl:attribute name="class">
          <xsl:call-template name="nodeTitleClass"/>
		</xsl:attribute>
		<xsl:attribute name="onmouseover">mouseOverNode(this);</xsl:attribute> 
		<xsl:attribute name="onmouseout">mouseOutNode(this);</xsl:attribute>
	    <xsl:attribute name="id"><xsl:value-of select="@revtree:id"/>Title</xsl:attribute>
        <xsl:attribute name="tabindex">-1</xsl:attribute>
		<xsl:value-of select="@role"/>
	  </span>
      <xsl:call-template name="detailsTable"/>
      <ul role="group">
        <xsl:if test="count(child::*)">
          <xsl:apply-templates/> 
        </xsl:if>
      </ul>
	</div>
  </li>
</xsl:template>

<xsl:template match="//accessible/@*">
  <span>
	<xsl:variable name="baseclass" 
                  select="concat('accessible', name())"/>
	<xsl:choose>
	  <xsl:when test="contains(../@revtree:updatedAttribs, name())">
		<xsl:attribute name="class">
		  <xsl:value-of select="concat($baseclass,' revUpdated')"/>
		</xsl:attribute> 
	  </xsl:when>

	  <xsl:when test="contains(../@revtree:deletedAttribs, name())">
		<xsl:attribute name="class">
		  <xsl:value-of select="concat($baseclass,' revDeleted')"/>
		</xsl:attribute> 
	  </xsl:when>

	  <xsl:when test="contains(../@revtree:insertedAttribs, name())">
		<xsl:attribute name="class">
		  <xsl:value-of select="concat($baseclass,' revInserted')"/>
		</xsl:attribute> 
	  </xsl:when>

	  <xsl:otherwise>
		<xsl:attribute name="class">
		  <xsl:value-of select="$baseclass"/>
		</xsl:attribute> 
	  </xsl:otherwise>

    </xsl:choose>
    <xsl:value-of select="." />
  </span>
</xsl:template>

<xsl:template name="detailsTable">
  <table class="accDetails" role="dialog">
    <tr>
      <td class="fieldname">Name:</td>
      <td class="fieldvalue"><xsl:apply-templates select="@name"/></td>
    </tr>
    <tr>
      <td class="fieldname">Role:</td>
      <td class="fieldvalue"><xsl:apply-templates select="@role"/></td>
    </tr>
    <tr>
      <td class="fieldname">Description:</td>
      <td class="fieldvalue"><xsl:apply-templates select="@description"/></td>
    </tr>
    <tr>
      <td class="fieldname">State:</td>
      <td class="fieldvalue"><xsl:apply-templates select="@state"/></td>
    </tr>
    <tr>
      <td class="fieldname">Value:</td>
      <td class="fieldvalue"><xsl:apply-templates select="@value"/></td>
    </tr>
    <tr>
      <td class="fieldname">Actions:</td>
      <td class="fieldvalue"><xsl:apply-templates select="@actions"/></td>
    </tr>
  </table>
</xsl:template>

<xsl:template name="labeledBy">
  <xsl:choose>
	<xsl:when test="contains(@revtree:changes, 'deleted-self')">labelDeleted</xsl:when>
	<xsl:when test="contains(@revtree:changes, 'inserted-self')">labelInserted</xsl:when>
	<xsl:when test="contains(@revtree:changes, 'updated-attrib')">labelAttribUpdate</xsl:when>
	<xsl:when test="contains(@revtree:changes, 'inserted-attrib')">labelAttribUpdate</xsl:when>
  </xsl:choose>
</xsl:template>

<xsl:template name="nodeTitleClass">
  nodeTitle
  <xsl:if test="contains(@revtree:changes, 'moved-self')">		
	revMoved
  </xsl:if>
  <xsl:if test="contains(@revtree:changes, 'deleted-self')">
	revDeleted
  </xsl:if>
  <xsl:if test="contains(@revtree:changes, 'inserted-self')">
	revInserted
  </xsl:if>
  <xsl:if test="contains(@revtree:changes, 'updated-attrib')">
	revAttribUpdate
  </xsl:if>
  <xsl:if test="contains(@revtree:changes, 'inserted-attrib')">
	revAttribUpdate
  </xsl:if>
</xsl:template>

<xsl:template name="itemClass">
  treeNode
  <xsl:choose>
    <xsl:when test="preceding-sibling::*">
      <xsl:choose>
        <xsl:when test="following-sibling::*">
          middle
        </xsl:when>
        <xsl:otherwise>
          last
        </xsl:otherwise>
      </xsl:choose>
    </xsl:when>
    <xsl:otherwise>
      <xsl:choose>
        <xsl:when test="following-sibling::*">
          first
        </xsl:when>
        <xsl:otherwise>
          single
        </xsl:otherwise>
    </xsl:choose>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

</xsl:stylesheet>
