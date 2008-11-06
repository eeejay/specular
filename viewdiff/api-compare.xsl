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
      <p>
        <span class="revInserted">Inserted</span><xsl:text> </xsl:text>
        <span class="revDeleted">Deleted</span><xsl:text> </xsl:text>
        <span class="revUpdated">Updated</span><xsl:text> </xsl:text>
        <span class="revMoved">Moved</span><br/>
        <span><b>[</b>name • role<b>]</b></span>
      </p>
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
    </body>
  </html>
</xsl:template>


<xsl:template match="left">
  <td width="%50">
    <ul>
      <xsl:apply-templates/> 
    </ul>
  </td>
</xsl:template>

<xsl:template match="right">
  <td width="%50">
    <ul>
      <xsl:apply-templates/> 
    </ul>
  </td>
</xsl:template>

<xsl:template match="accessible">
  <li>
    <xsl:attribute name="class">
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
          </xsl:choose>        </xsl:otherwise>
      </xsl:choose>
    </xsl:attribute>
	<div>
    <span>
      <xsl:attribute name="class">
        accessiblenode
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
      </xsl:attribute>
	  <xsl:attribute name="onclick">showDetails(this);</xsl:attribute> 
	  <xsl:if test="@revtree:id">
	    <xsl:attribute name="id">
		  <xsl:value-of select="@revtree:id"/>
	    </xsl:attribute>
	  </xsl:if>
      <span class="nodeTitle">
		<xsl:attribute name="onmouseover">highlightNode(this);</xsl:attribute> 
		<xsl:attribute name="onmouseout">unhighlightNode(this);</xsl:attribute>
		<xsl:if test="@revtree:id">
	      <xsl:attribute name="id">
			<xsl:value-of select="@revtree:id"/>Title
	      </xsl:attribute>
		</xsl:if>
		<xsl:value-of select="@role"/>
	  </span>
      <table class="accDetails">
        <tr>
          <td class="fieldname">Name:</td>
          <td><xsl:apply-templates select="@name"/></td>
        </tr>
        <tr>
          <td class="fieldname">Role:</td>
          <td><xsl:apply-templates select="@role"/></td>
        </tr>
        <tr>
          <td class="fieldname">Description:</td>
          <td><xsl:apply-templates select="@description"/></td>
        </tr>
        <tr>
          <td class="fieldname">State:</td>
          <td><xsl:apply-templates select="@state"/></td>
        </tr>
        <tr>
          <td class="fieldname">Value:</td>
          <td><xsl:apply-templates select="@value"/></td>
        </tr>
        <tr>
          <td class="fieldname">Actions:</td>
          <td><xsl:apply-templates select="@actions"/></td>
        </tr>
      </table>
	</span>
    <xsl:if test="count(child::*)">
      <ul>
        <xsl:apply-templates/> 
      </ul>
    </xsl:if>
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
</xsl:stylesheet>
